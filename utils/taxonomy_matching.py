import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def match_skills_to_taxonomy(skill_embeddings, taxonomy_embeddings, taxonomy_names, top_k):

    results = []
    for emb in skill_embeddings:
        # 2) Compute similarities for this text
        sims = cosine_similarity([emb], taxonomy_embeddings)[0]

        # 3) Pick the top-K most similar skill indices
        top_idxs = np.argpartition(sims, -top_k)[-top_k:]
        top_idxs = top_idxs[np.argsort(sims[top_idxs])[::-1]]

        # 4) Map to (skill_name, score) tuples
        top_skills_with_scores = [
            (taxonomy_names[idx].replace("\u00a0", " "), float(sims[idx]))
            for idx in top_idxs
        ]
        results.append(top_skills_with_scores)

    return results







# from utils import embed
# from utils import load_skill_embeddings

# # Load skill embeddings and names once
# base_dir = os.path.dirname(__file__)
# embed_path = os.path.join(base_dir, "data", "ESCO_embeddings_single_string.pkl")
# skill_embeddings, skill_names = load_skill_embeddings.load_skill_embeddings(embed_path)

# def extract_skills_from_texts(texts: list[str], top_k_skills: int = 10
# ) -> list[list[tuple[str, float]]]:
#     """
#     Embed all input texts in one call, then for each embedding compute cosine
#     similarity against preloaded skill embeddings and return the top_k_skills.
#     """
#     # 1) Batch-embed all texts at once for speed
#     embeddings = embed.openai_embed(texts)  # returns list of vectors

#     results: list[list[tuple[str, float]]] = []
#     for emb in embeddings:
#         # 2) Compute similarities for this text
#         sims = cosine_similarity([emb], skill_embeddings)[0]

#         # 3) Pick the top-K most similar skill indices
#         top_idxs = np.argpartition(sims, -top_k_skills)[-top_k_skills:]
#         top_idxs = top_idxs[np.argsort(sims[top_idxs])[::-1]]

#         # 4) Map to (skill_name, score) tuples
#         top_skills_with_scores = [
#             (skill_names[idx].replace("\u00a0", " "), float(sims[idx]))
#             for idx in top_idxs
#         ]
#         results.append(top_skills_with_scores)

#     return results




# list = ['planning', 'organizing', 'monitoring all maintenance operation activities', 'provide a safe and efficient highway system.  ', 'organize directs the program', 'management and supervision of several Division 10’s Maintenance Units, oversight and management of the Division’s Contract Resurfacing and Preservation Programs', 'developing and maintaining HMIP.  ', 'Division lead representative', 'troubleshoot issues', 'coordinate with management on solutions', 'implements direct technical and administrative support to all Engineers , Managers , and Supervisors', 'provides direct technical and administrative support to all Engineers , Managers , and Supervisors', 'technical and administrative support', 'Responds to inquiries', 'DOT policies and procedures', 'Division maintenance projects', 'Management prefers applicants', 'Knowledge and understanding of engineering concepts, maintenance practices and theories used in maintenance of all roadway assets', 'planning', 'developing', 'tracking', 'engineering analysis', 'preparing technical, statistical, and managerial reports', 'supervising, motivating, counseling, and training other engineers and technicians Experience collaborating with others', 'maintaining effective working relationships', 'providing updates to management', 'establish and maintain effective working relationships', 'identify problems', 'report potential problems', 'communicate and implement new policies and procedures', 'prepare and organize written reports', 'review written reports', 'guide staff', 'acquire basic understanding of working relationships', 'act as representative', 'guide for detail', 'answer all questions associated with the application']
# results = []

# for val in list:
#     # print(val[1])
#     results.append(extract_skills_from_text(val, top_k_skills=2)[0][0])


# print(results)
