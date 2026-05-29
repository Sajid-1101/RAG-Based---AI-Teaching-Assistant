import os
import re
import subprocess
import sys
from flask import Flask, render_template, request, flash, send_from_directory, Response, abort

app = Flask(__name__)
app.secret_key = os.urandom(24)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.normpath(os.path.join(APP_DIR, '..', 'initial', 'merged_jsons'))
VIDEO_DIR = os.path.normpath(os.path.join(APP_DIR, '..', 'initial', 'videos'))


def normalize_sample_title(raw_title: str) -> str:
    if raw_title.endswith('.mp3'):
        raw_title = raw_title[:-4]
    if '_' in raw_title:
        parts = raw_title.split('_', 1)
        raw_title = f"{parts[0]}. {parts[1].replace('_', ' ')}"
    return raw_title


def load_samples():
    samples = []
    if os.path.isdir(SAMPLES_DIR):
        for file_name in sorted(os.listdir(SAMPLES_DIR)):
            if file_name.endswith('.json'):
                title = os.path.splitext(file_name)[0]
                title = normalize_sample_title(title)
                samples.append({
                    'title': title,
                    'file_name': file_name,
                })
    return samples


def load_videos():
    videos = []
    if os.path.isdir(VIDEO_DIR):
        for file_name in sorted(os.listdir(VIDEO_DIR)):
            if file_name.lower().endswith(('.mp4', '.webm', '.ogg')):
                title = os.path.splitext(file_name)[0]
                videos.append({
                    'title': title,
                    'file_name': file_name,
                })
    return videos


def load_external_video_map():
    """Load optional external video URL mapping from `external_videos.json`.
    The JSON should map video title -> external URL.
    """
    mapping_path = os.path.join(APP_DIR, 'external_videos.json')
    if not os.path.isfile(mapping_path):
        return {}
    try:
        import json
        with open(mapping_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def get_external_player_url(url: str) -> str:
    if not url:
        return ''
    if 'player.cloudinary.com/embed/' in url:
        return url

    match = re.search(
        r'https://res\.cloudinary\.com/([^/]+)/video/upload/(?:v\d+/)?(?:[^/]+/)*(.+?)\.(ts|mp4|webm)(?:\?.*)?$',
        url,
    )
    if match:
        cloud_name, public_id, _ = match.groups()
        return (
            f'https://player.cloudinary.com/embed/?cloud_name={cloud_name}'
            f'&public_id={public_id}&resource_type=video'
        )

    return url


@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = None
    user_prompt = ''
    if request.method == 'POST':
        user_prompt = request.form.get('prompt', '').strip()
        if user_prompt:
            response_text = run_process_incoming(user_prompt)
        else:
            flash('Please enter a prompt before submitting.', 'warning')
    samples = load_samples()
    external_map = load_external_video_map()
    # attach external_url and a Cloudinary player URL when available
    for sample in samples:
        external_url = external_map.get(sample['title'], '')
        sample['external_url'] = external_url
        sample['external_player_url'] = get_external_player_url(external_url)
    return render_template(
        'index.html',
        samples=samples,
        response=response_text,
        prompt=user_prompt,
    )


def run_process_incoming(user_prompt: str) -> str:
    script_path = os.path.join(APP_DIR, 'process_incoming.py')
    response_file = os.path.join(APP_DIR, 'response.txt')

    if not os.path.exists(script_path):
        return 'Error: process_incoming.py not found in the app folder.'

    try:
        completed = subprocess.run(
            [sys.executable, script_path],
            input=user_prompt + '\n',
            cwd=APP_DIR,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return 'Error: processing timed out. Please try again.'

    if completed.returncode != 0:
        error_message = completed.stderr.strip() or completed.stdout.strip()
        return f'Error running processing_incoming: {error_message}'

    if not os.path.exists(response_file):
        return 'Error: response.txt was not created by processing_incoming.'

    with open(response_file, 'r', encoding='utf-8') as f:
        return f.read().strip()


@app.route('/videos/<path:filename>')
def video_file(filename):
    path = os.path.join(VIDEO_DIR, filename)
    if not os.path.isfile(path):
        abort(404)

    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_from_directory(VIDEO_DIR, filename)

    size = os.path.getsize(path)
    byte1 = 0
    byte2 = None
    match = re.search(r'bytes=(\d+)-(\d*)', range_header)
    if match:
        groups = match.groups()
        byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])

    if byte2 is None or byte2 >= size:
        byte2 = size - 1

    length = byte2 - byte1 + 1
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    response = Response(data, 206, mimetype='video/mp4', direct_passthrough=True)
    response.headers.add('Content-Range', f'bytes {byte1}-{byte2}/{size}')
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Content-Length', str(length))
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
