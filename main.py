from lib.read_file import read_cv
from lib.llm import extract_cv
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
import instructor
import json
import os

load_dotenv()


def main():
    # Configure Groq API
    groq_api_key = os.getenv("GROQ_API_KEY")
    cv_path = "CV_sans_profil.pdf"
    # cv_path = "cv_word.docx"
    # cv_path = "cv.txt"

    cv_text = read_cv(cv_path)

    client = instructor.from_groq(Groq(), mode=instructor.Mode.JSON)

    sys_prompt = """Tu es une IA experte dans l'analyse des CV de candidats. 

    J'aimerais analyser le CV d'un candidat et savoir quelle est son profil.

    Ta tâche sera d'abord d'extraire les informations du CV sous formes de sections en suivant la structure du JSON Schema Raisonnement  puis d'en déduire le profil du candidat dans "reponse_finale".

    Tu extrairas les informations du CV et n'inventeras pas d'informations, il est très important que tu suives la structure du Schéma Pydantic donné en paramètre !"""

    input_prompt = f"""
    Contenu du CV brut : {cv_text}

    Réponse :
    """

    response = extract_cv(client, sys_prompt, input_prompt)
    if response:
        response = json.loads(response.model_dump_json())
    else:
        print("Error parsing the resume.")

    df_formations = pd.DataFrame(response["extraction_cv"]["formations"])
    df_formations = df_formations.rename(
        columns={"dates": "Dates", "intitule_formation": "Formation", "ecole": "Ecole"}
    )

    df_experiences = pd.DataFrame(response["extraction_cv"]["experiences"])
    df_experiences = df_experiences.rename(
        columns={
            "dates": "Dates",
            "nom_entreprise": "Entreprise",
            "intitule_poste": "Poste",
            "missions": "Missions",
        }
    )

    df_competences = pd.DataFrame(response["extraction_cv"]["competences"])
    df_competences = df_competences.rename(
        columns={"nom_competence": "Competence", "niveau": "Niveau"}
    )

    df_langues = pd.DataFrame(response["extraction_cv"]["langues"])
    df_langues = df_langues.rename(columns={"langue": "Langue", "niveau": "Niveau"})

    df_centres_interets = pd.DataFrame(response["extraction_cv"]["centres_interets"])
    df_centres_interets = df_centres_interets.rename(
        columns={"type_hobby": "Catégorie", "nom_hobby": "Hobby"}
    )

    del response["extraction_cv"]["formations"]
    del response["extraction_cv"]["experiences"]
    del response["extraction_cv"]["competences"]
    del response["extraction_cv"]["centres_interets"]
    del response["extraction_cv"]["langues"]

    df_informations = pd.DataFrame(response["extraction_cv"], index=[0])
    df_informations = df_informations.rename(
        columns={
            "nom": "Nom",
            "prenom": "Prenom",
            "email": "Email",
            "adresse": "Adresse",
            "linkedin": "Profil linkedin",
        }
    )

    print("Profil du candidat :\n", response["reponse_finale"])
    print("Informations générales :\n", df_informations)
    print("Formation :\n", df_formations)
    print("Expérience professionnelles :\n", df_experiences)
    print("Compétences :\n", df_competences)
    print("Langues :\n", df_langues)
    print("Hobbies :\n", df_centres_interets)


if __name__ == "__main__":
    main()
