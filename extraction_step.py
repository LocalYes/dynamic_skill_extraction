from utils.skill_extraction import chatgpt_skills_extraction
from utils.embed import openai_embed
from utils.load_embeddings import load_skill_embeddings
from utils.taxonomy_matching import match_skills_to_taxonomy
from utils.skill_filtering import chatgpt_skills_filtering

import copy
import numpy as np

def skill_extraction_step(text, PARAMS):
    #print("Extracting skills")
    extracted_skills = chatgpt_skills_extraction(text, PARAMS["extract_model"], PARAMS["client"])['skills']

    embedded_skills = openai_embed(extracted_skills, PARAMS["embed_model"], PARAMS["client"])
    embedded_skills = np.array(embedded_skills)

    #print("Embedding skills")
    taxonomy_embeddings, taxonomy_names = load_skill_embeddings(PARAMS["skills_embed_data"])

    matches_sub_skills_list = match_skills_to_taxonomy(embedded_skills, taxonomy_embeddings, taxonomy_names, PARAMS["topk"])
    matched_skills = []
    for matches_sub_skills in matches_sub_skills_list: matched_skills.extend(matches_sub_skills)

    matched_skills = list(set([skill[0] for skill in matched_skills]))

    #print("Filtering skills")
    filtered_skills = chatgpt_skills_filtering(text, matched_skills, PARAMS["extract_model"], PARAMS["client"])['skills']

    return [str.lower(skill) for skill in filtered_skills]
    


