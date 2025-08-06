def init_client():
    from openai import OpenAI
    import os

    base_dir = os.path.dirname(__file__) 
    parent_dir = os.path.abspath(os.path.join(base_dir, ".."))
    key_path = os.path.join(parent_dir, "OPENAI_KEY.txt")

    return OpenAI(api_key=open(key_path).read().strip())

def openai_embed(to_embed, model="text-embedding-3-large", client=False):
    if not client:
        client = init_client()

    if isinstance(to_embed, str):
        inputs = [to_embed]
    elif isinstance(to_embed, list) and all(isinstance(x, str) for x in to_embed):
        inputs = to_embed
    else:
        raise ValueError("openai_embed input must be a string or list of strings")

    response = client.embeddings.create(
        input=inputs,
        model=model
    )

    embeddings = [d.embedding for d in response.data]
    return embeddings[0] if isinstance(to_embed, str) else embeddings