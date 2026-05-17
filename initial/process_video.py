import os
import subprocess

files = os.listdir('videos')
for file in files:
    print(file)
    file_no = file.split('. ')[0]
    filename = file.split('. ')[1].split('.')[0]
    print(file_no,filename)
    subprocess.run(['ffmpeg','-i',f"videos/{file}", f"audios/{file_no}_{filename}.mp3"])