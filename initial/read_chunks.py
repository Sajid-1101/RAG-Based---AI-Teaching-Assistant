import requests
import json
import pandas as pd
import os
import joblib

def create_embedding(text_list):
    r= requests.post("http://localhost:11434/api/embed", json={
    "model": "bge-m3",
    "input": text_list,
    })
    embedding = r.json()['embeddings']
    return embedding
    # return 2d list : [[q1],[q2],....]

jsons = os.listdir("jsons")
my_dict = []
chunk_id = 0

for json_file in jsons:
    with open(f"jsons/{json_file}") as f:
        content = json.load(f)
    print(f"creating embedding for {json_file}")
    embeddings = create_embedding([c['text'] for c in content['chunks']])
    for i, chunk in enumerate(content['chunks']):
        # adding id & embedding to json content
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk_id += 1
        my_dict.append(chunk)
# print(my_dict)

df = pd.DataFrame.from_records(my_dict)
# save the dataframe using joblib 
joblib.dump(df,'../app/embedding.joblib')
