Projet extraction du CV et déduction du profil du candidat.
Programme utilisant l'IA Générative afin d'extraire les informations du candidat sous forme de sections :
- Informations personnelles (nom, prénom, email etc.)
- Formations
- Expériences professionnelles
- Compétences
- Langues
- Hobbies

Ensuite, l'IA en déduira le profil de l'utilisateur en fonction de son parcours.
Ce programme n'accepte que les fichiers PDF, peut être facilement adapté au format Word (voir notebook).

L'anonymisation des données du CV est importante car les informations envoyés à l'IA Générative peuvent représenter un problème de RGPD pour les utilisateurs. 

L'anonymisation a été testé sur le notebook d'exploration avec GLiNER et les résultats sont assez bons surtout concernant le nom/prénom. Les données à anonymiser sont nom/prénom, adresse, email, numéro de téléphone mais on peut ajouter plusieurs catégories supplémentaires.

L'anonymisation est fonctionnelle mais seulement sur le notebook, cette étape apporte une latence supplémentaire dans le traitement des CV donc à voir s'il est viable en production ou si un modèle d'anonymisation moins coûteux en puissance de calcul est nécessaire.

Comment utiliser ce programme ?

###  Pré-requis :
 - Python 3.10+ (idéalement 3.12.6)
 - Git (Gestion de versions)
 - Créer un compte sur Groq (console.groq.com) et obtenir une clé d'accès API dans menu -> API Keys -> Create API Key -> Sauvegarder dans un fichier quelque part la clé API (suite de chiffres et lettres)

```bash
# Cloner le repo distant
git clone https://github.com/dracoeau/profil_cv.git

# Création de l'environnement virtuel
python -m venv myenv

# Installation de toutes les dépendances nécessaires au bon fonctionnement du projet
pip install -r requirements.txt
```

Créer un fichier qui se nomme .env à la racine du projet
Dans ce fichier mettre :

```bash
GROQ_API_KEY="la valeur de votre clé api"
```

### Lancer le code avec résultat en local sur le terminal

```bash
python main.py
```

### Lancer la démo sur le site Web avec streamlit

Utiliser la commande suivante dans le terminal à la racine du projet :
```bash
streamlit run demo.py
```
