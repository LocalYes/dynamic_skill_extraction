import json

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

def chatgpt_skills_extraction(description, gpt_model="gpt-4.1-mini", cliet=False):
    # Init client
    if not cliet: cliet = init_client()

    # text_list and skills_list must be parallel lists.
    #print("1. analytical step")

    analytical_messages = [
        {"role": "system", "content": '''
            You are a job description analyst and skill extractor. You analyze job postings to extract their underlying required skills, expressed in the style and granularity of the ESCO (European Skills, Competences, Qualifications and Occupations) taxonomy.
            You ensure high coverage by considering not only technical and managerial requirements, but also public sector competencies, program and contract management, stakeholder engagement, reporting, regulatory compliance, disaster/emergency coordination, and use of any named software or systems.
            If you need to mention a software name (eg. "SQL", "Power BI", "SAP", "BEACON"), only mention the software name, without filler words. For example, simply say "SQL", "BEACON", "Excel"

            Example skills to provide:
            1. SQL
            2. Work in teams
            3. Protfolio management
            4. Power BI
         
            You also follow a two-step approach:
            First, analyze and summarize the key responsibilities and requirements of the job, sector-specific, regulatory and reporting obligations, and coordination with external agencies.
            Second, extract a Python list of the core skills involved. Ensure each skill is clear, such as. program management, contract management, disaster response, public communication, inter-agency coordination, compliance, technical expertise, stakeholder engagement.
        '''},
        {"role": "user", "content": f'''
            Please analyze the following job description and extract the underlying skills, following this format:

            Step 1: Provide a concise analysis of the main job responsibilities, required experience, and expected competencies, with special attention to public sector, program management, reporting, regulatory, and disaster/emergency tasks.
            Step 2: Extract a Python list of the underlying skills, written in the ESCO skill style.

            Job Description:
            {description}

        '''}
    ]


    analytical_responce = chatgpt_send_messages(analytical_messages, gpt_model, cliet)


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

    json_skills = chatgpt_send_messages_json(json_messages, json_schema, "gpt-4.1-nano", cliet)

    return json_skills
