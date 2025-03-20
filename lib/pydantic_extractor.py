from pydantic import BaseModel, Field
from typing import List

default = ""

class Formation(BaseModel):
    """Formations que le candidat a suivi"""
    dates: str = Field(default=default)
    intitule_formation: str = Field(default=default)
    ecole: str = Field(default=default)

class Experience(BaseModel):
    """Expériences professionnelles du candidat"""
    dates: str = Field(default=default)
    nom_entreprise: str = Field(default=default)
    intitule_poste: str = Field(default=default)
    missions: List[str] = Field(default=[])

class Competence(BaseModel):
    """Compétence du candidat"""
    nom_competence: str = Field(default=default)
    niveau: str = Field(default=default)

class Langue(BaseModel):
    langue: str = Field(default=default)
    niveau: str = Field(default=default)

class Hobby(BaseModel):
    type_hobby: str = Field(default=default)
    nom_hobby: str = Field(default=default)

class CvExtractor(BaseModel):
    """Informations à extraire du CV du candidat"""
    nom: str = Field(default=default)
    prenom: str = Field(default=default)
    email: str = Field(default=default)
    adresse: str = Field(default=default)
    linkedin: str = Field(default=default)
    formations: List[Formation]
    experiences: List[Experience]
    competences: List[Competence]
    langues: List[Langue]
    centres_interets: List[Hobby]

class Raisonnement(BaseModel):
    extraction_cv: CvExtractor
    reponse_finale: str = Field(description="profil du candidat écrit en français en fonction des informations extraites du CV")