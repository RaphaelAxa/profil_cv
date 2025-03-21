from lib.pydantic_extractor import Raisonnement


def extract_cv(client, sys_prompt, input_prompt):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": input_prompt},
            ],
            # model="llama3-8b-8192",
            model="llama-3.3-70b-versatile",
            response_model=Raisonnement,
        )
        return response
    except Exception as e:
        print(f"Erreur dans l'analyse du CV : {e}")
        return None
