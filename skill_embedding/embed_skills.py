import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from aiskills.utils.embed import openai_embed
import numpy as np
import pickle

"""
def embed_in_batches(skills, batch_size=1000):
    embeddings_batches = []
    for start in range(0, len(skills), batch_size):
        end = start + batch_size
        batch = skills[start:end]
        print(f"Embedding skills ( {end-1} / {len(skills)})")
        emb = openai_embed(batch)
        embeddings_batches.append(emb)

    return np.concatenate(embeddings_batches, axis=0)
# 49 / 13300
# 0.00737 / 13300

def save_skill_embeddings(embeddings, names, path):
    all_skills = []
    for emb, name in zip(embeddings, names):
        skill_dict = [
            emb,
            name
        ]
        all_skills.append(skill_dict)

    with open(path, "wb") as f:
        pickle.dump(all_skills, f)
"""


def embed_and_save_in_batches(skills, batch_size, names, save_path):
    with open(save_path, "wb") as f:
        for start in range(0, len(skills), batch_size):
            end = min(start + batch_size, len(skills))
            batch = skills[start:end]
            print(f"Embedding skills ( {end-1} / {len(skills)})")
            embeddings = openai_embed(batch)
            batch_skills = [[emb, name] for emb, name in zip(embeddings, names[start:end])]
            pickle.dump(batch_skills, f)

if __name__ == "__main__":
    skills_list = []
    dict = r"C:\Users\artio\OneDrive\Desktop\dynamic_skill_extraction\data"
    save_name = "ESCO_skills_ONET_skills" + ".pkl"
    
    # Logic for extracting skill from a data source goes here:

    import json
    with open(r"C:\Users\artio\OneDrive\Desktop\dynamic_skill_extraction\skill_embedding\raw_data\ESCO_hierarchies.json", "r") as file:
        hierarchies = json.load(file)

    for hierarchy in hierarchies:
        skills_list.append(hierarchy["hierarchy"][-1])

    # +++++ The ONET Technology used data

    with open(r"C:\Users\artio\OneDrive\Desktop\dynamic_skill_extraction\skill_embedding\raw_data\ONET_skills.json", "r") as file:
        onet_skills = json.load(file)
    
    skills_list.extend(onet_skills)

    skills_list = list(set(skills_list))

    # end

    print(f"Embedding {len(skills_list)} skills")
    print(f"Estimate processing duration (only API): {round(0.368421 * (len(skills_list) / 100), 3)}s")
    print(f"Estimate processing cost (only API): ${round(0.00737854 * (len(skills_list) / 13300), 6)}")

    save_path = os.path.join(dict, save_name)
    embed_and_save_in_batches(skills_list, 1000, skills_list, save_path)

