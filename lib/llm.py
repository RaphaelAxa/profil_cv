from lib.pydantic_extractor import Raisonnement

def extract_cv(client, sys_prompt, input_prompt):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role":"user", "content": input_prompt}
            ],
            model="mixtral-8x7b-32768",
            response_model=Raisonnement,
        )
        return response
    except Exception as e:
        print(f"Erreur dans l'analyse du CV : {e}")
        return None
