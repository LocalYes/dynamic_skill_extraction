import json
import time


def chatgpt_send_messages(messages, model, client):
    analytical_response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return analytical_response.choices[0].message.content

def chatgpt_send_messages_json(messages, json_schema, model, client):
    json_response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "responce_retrieval",
                "strict": True,
                "schema": json_schema
            }
        }
    )

    json_response_content = json_response.choices[0].message.content
    return json.loads(json_response_content)

def init_client():
    from openai import OpenAI
    import os

    base_dir = os.path.dirname(__file__) 
    parent_dir = os.path.abspath(os.path.join(base_dir, ".."))
    key_path = os.path.join(parent_dir, "OPENAI_KEY.txt")

    return OpenAI(api_key=open(key_path).read().strip())

def chatgpt_skills_filtering(text, skills, gpt_model="gpt-4.1-mini", client=False):
    # Init client
    if not client: clinet = init_client()

    #print("1. analytical step")

    analytical_messages = [
        {"role": "system", "content": '''
            You are a skills evaluator tasked with determining the alignment between a set of predefined skills and a provided job or course description. Your role is to classify and filter only the skills given — do not invent, reword, generalize, or add any new skills. Only work with the skill list exactly as it is provided.

            Follow the instructions below strictly:

            1. Highly Relevant Skills
            List only the skills from the provided list that are clearly aligned with the job or course. These skills should either be explicitly mentioned or strongly implied in the description.

            2. Possibly Relevant but Less Central
            List only the provided skills that might apply indirectly, support secondary functions, or are related but not essential. Do not assume or stretch relevance beyond what is supported by the description.

            3. Irrelevant or Misaligned Skills
            List the provided skills that do not match the description in terms of domain, responsibility, or relevance. Include skills that may belong to different professions or are out of scope.

            4. Final Refined Skill List
            Create a final list only using the exact skill phrases from the provided list. Choose skills only from section 1 and, if clearly justifiable, a few from section 2. You must not edit, rephrase, or invent any new skills.

            Format the final list using this structure:

            1. skill 1
            2. skill 2
            ...
            Do not use underscores or change the skill wording in any way.
            Do not add emojis, summaries, or explanations outside the structure.
        '''},
        {"role": "user", "content": f'''
            TEXT:
            {text}

            PREDICTED SKILLS (PROVIDED LIST):
            {skills}
        '''}
    ]

    analytical_responce = chatgpt_send_messages(analytical_messages, gpt_model, client)

    #print("2. jsonification step")

    json_messages = [
        {"role": "system", "content": """
            You are a JSON transformation assistant.
            Your task is to read the user's input, which contains a list of final skills (typically formatted in Python-style or plain text), and convert it into a valid, JSON structure, obeying the json schema.

            Objective:
            1. Extract the final list of skills from user input, and output the list of skills acording to the json schema.
            2. Copy the skills letter to letter, no additional corrections or capitalization. 

            Avoid emojis or unnecessary commentary. Please copy the skill letter to letter, NO "_".
        """},
        {"role": "user", "content": f"""
            {analytical_responce}
        """}
    ]

    json_schema = {
        "type": "object",
        "properties": {
            "skills": {
                "type": "array",
                "items": { "type": "string" }
            }
        },
        "required": ["skills"],
        "additionalProperties": False
    }

    filtered_skills = chatgpt_send_messages_json(json_messages, json_schema, "gpt-4.1-nano", client)

    return filtered_skills
