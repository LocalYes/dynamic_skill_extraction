excel_list = [
    ("https://www.onetcenter.org/dl_files/database/db_29_3_excel/Knowledge.xlsx", "Element Name"),
    ("https://www.onetcenter.org/dl_files/database/db_29_3_excel/Skills.xlsx", "Element Name"),
    ("https://www.onetcenter.org/dl_files/database/db_29_3_excel/Abilities.xlsx", "Element Name"),
    ("https://www.onetcenter.org/dl_files/database/db_29_3_excel/Technology%20Skills.xlsx", "Example"),
    ("https://www.onetcenter.org/dl_files/database/db_29_3_excel/Tools%20Used.xlsx", "Example"),
    ("https://www.onetcenter.org/dl_files/database/db_29_3_excel/Skills%20to%20Work%20Activities.xlsx", "Work Activities Element Name"),   # might be too general
    ("https://www.onetcenter.org/dl_files/database/db_29_3_excel/Abilities%20to%20Work%20Activities.xlsx", "Work Activities Element Name")
]


import pandas as pd

def extract_column(url, column):
    df = pd.read_excel(url)
    return df[column].drop_duplicates().dropna().tolist()

all_skills = []

for excel in excel_list:
    all_skills.extend(extract_column(excel[0], excel[1]))
    print("Done 1")

all_skills = list(set(all_skills))

#print(all_skills)
print(len(all_skills))


import json

with open(r"C:\Users\artio\OneDrive\Desktop\dynamic_skill_extraction\skill_embedding\raw_data\ONET_scraped.json", "w") as file:
    json.dump(all_skills, file, indent=4)



