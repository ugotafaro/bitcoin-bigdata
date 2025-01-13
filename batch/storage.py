import json
import os

from pymongo import MongoClient

# Connexion à MongoDB (remplace avec tes informations de connexion)
# Load environment variables from .env file



# Get the auth token from the environment variable



uri = f"mongodb+srv://utafaro:BiSjjiYSm1THEKKl@cluster0.l71ap.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


try:
    client = MongoClient(uri)
    print("Connexion à MongoDB réussie !")
except Exception as e:
    print(f"Erreur de connexion à MongoDB : {e}")

# Accéder à la base de données et à la collection
db = client["bitcoin-data"]  # Nom de la base de données
collection = db["bitcoin-batch"]  # Nom de la collection

# Chemin du fichier JSON à lire (ligne par ligne)
file_path = "processData.json"

# Lire et insérer chaque ligne du fichier JSON
# Lire et insérer chaque ligne du fichier JSON
with open(file_path, "r") as file:
        for line in file:
            print("Ligne en cours de traitement :", line)
            # Charger chaque ligne comme un objet JSON
            data = json.loads(line.strip())
            
            # Insérer l'objet JSON dans la collection MongoDB
            insert_result = collection.insert_one(data)
            print(f"Document inséré avec ID : {insert_result.inserted_id}")

client.close()