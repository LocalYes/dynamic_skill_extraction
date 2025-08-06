import os
import pickle
import numpy as np

def load_skill_embeddings(embedding_file_name):
    base_dir = os.path.dirname(__file__) 
    embed_path = os.path.join(base_dir, "..", "data", embedding_file_name)
    
    skill_embeddings = []
    skill_names = []

    with open(embed_path, "rb") as f:
        all_skills = pickle.load(f)

    for skill in all_skills:
        skill_embeddings.append(skill[0])
        skill_names.append(skill[1])

    return np.array(skill_embeddings), skill_names




