import os
import math
import json

n = 5

for filename in os.listdir("jsons"):
    if filename.endswith(".json"):
        with open(os.path.join("jsons", filename), "r") as f:
            data = json.load(f)
        
            num_chunks = len(data["chunks"])
            new_chunks = []
            num_grp = math.ceil(num_chunks / n)
            
            for i in range(num_grp):
                start_idx = i * n
                end_idx = min((i + 1) * n, num_chunks)
                
                chunk_group = data["chunks"][start_idx:end_idx]
                new_chunks.append({
                    "number" : data['chunks'][0]['number'],
                    "title" : data['chunks'][0]['title'],
                    "start" : chunk_group[0]['start'],
                    "end" : chunk_group[-1]['end'],
                    "text" : " ".join([chunk['text'] for chunk in chunk_group])
                })
        os.makedirs("merged_jsons", exist_ok=True)
        with open(os.path.join("merged_jsons", filename), "w") as json_file:
            json.dump({"chunks": new_chunks , "text" : data["text"]}, json_file, indent=4)
                