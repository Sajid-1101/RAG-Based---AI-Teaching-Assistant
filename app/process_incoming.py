import joblib
import pandas as pd
import requests
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from config import api_key
# using bge-m3 for embedding
def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
    "model": "bge-m3",
    "input": text_list,
    })
    embedding = r.json()['embeddings']
    return embedding
# using llama3.2 for inference
# def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2",
    "prompt": prompt,
    "stream": False,
    })
    response = r.json()
    return response
# using gemini for inference
def inference_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    # Structure the payload exactly how Gemini expects it
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    # Make the POST request
    r = requests.post(url, json=payload)
    response = r.json()

    # Extract and return only the text response string
    try:
        return response["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return f"Error: {response}"

df = joblib.load('embedding.joblib')

incoming_query = input("Ask a Question: ")
print("Processing your query...")
question_embedding = create_embedding([incoming_query])[0]

similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
top_results = 5
max_idx = similarities.argsort()[::-1][0:top_results]
new_df = df.loc[max_idx]

prompt = f"""
You are an AI tutor helping students find answers from course videos.

Answer ONLY from the provided context.
If the answer exists, mention:
- the exact video number
- the video title
- a short direct explanation

If the answer is not clearly available in the context, say:
"The topic is not clearly covered in the retrieved lessons."

Keep the answer concise and accurate.
----------------------------------------------
 Here are video subtitle chunks containing video title, video number, start time, end time in seconds, the text at that time : 
{new_df[['title','number','start','end','text']].to_json(orient = 'records')}
----------------------------------------
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (and at which timestamp , in min:sec format) and guide the user to go to that particular video. If user asks unrelated question(apart from html), tell him that you can only answer questions related to the course.
"""
with open('prompt.txt','w') as f:
    f.write(prompt)
    
# response = inference(prompt)['response']
response = inference_gemini(prompt)
print("response : ", response)
with open('response.txt','w') as f:
    f.write(response)
