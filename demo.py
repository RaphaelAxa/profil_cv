from langchain_community.document_loaders import PyPDFLoader
from streamlit_pdf_viewer import pdf_viewer
from lib.read_file import read_cv
from lib.llm import extract_cv
import streamlit as st
from groq import Groq
import pandas as pd
from pathlib import Path
import instructor
import tempfile
import json


def main():
    st.write("""
    # Extraction d'informations de CVs et génération du profil
    Pour l'association Entourage et la partie Entourage Pro
    """)

    # Configure Groq API
    uploaded_file = st.file_uploader("Importer votre CV", type=["pdf", "docx"])

    if uploaded_file:
        extension = Path(uploaded_file.name).suffix
        binary_data = uploaded_file.getvalue()
        if extension == ".pdf":
            pdf_viewer(input=binary_data, width=700)

        with tempfile.NamedTemporaryFile(
            suffix=extension, dir=".", mode="wb", delete=False
        ) as fp:
            fp.write(binary_data)
            temp_file = fp.name

        cv_text = read_cv(temp_file)
        fp.close()

        client = instructor.from_groq(
            Groq(api_key=st.secrets.GROQ_API_KEY), mode=instructor.Mode.JSON
        )

        sys_prompt = """Tu es une IA experte dans l'analyse des CV de candidats. 

        J'aimerais analyser le CV d'un candidat et savoir quelle est son profil.

        Ta tâche sera d'abord d'extraire les informations du CV sous formes de sections en suivant la structure du JSON Schema Raisonnement puis d'en déduire le profil du candidat dans "reponse_finale".

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
            columns={
                "dates": "Dates",
                "intitule_formation": "Formation",
                "ecole": "Ecole",
            }
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

        df_centres_interets = pd.DataFrame(
            response["extraction_cv"]["centres_interets"]
        )
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

        st.write("## Profil du candidat :")
        st.write(response["reponse_finale"])
        st.write("## Informations extraites du CV :")
        st.write("### Informations personnelles du candidat :")
        st.dataframe(df_informations)
        st.write("### Formations suivies par le candidat :")
        st.dataframe(df_formations)
        st.write("### Expériences professionnelles du candidat :")
        st.dataframe(df_experiences)
        st.write("### Compétences du candidat :")
        st.dataframe(df_competences)
        st.write("### Langues :")
        st.dataframe(df_langues)
        st.write("### Hobbies :")
        st.dataframe(df_centres_interets)


if __name__ == "__main__":
    main()
