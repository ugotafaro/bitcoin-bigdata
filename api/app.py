from flask import Flask, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from dotenv import load_dotenv
import pymongo
import requests
import time
import os

load_dotenv()

mongodb_url = os.getenv("DATABASE_URL")

app = Flask(__name__)
CORS(app)  # Autoriser les appels depuis le frontend React

client = pymongo.MongoClient(mongodb_url)
db = client["bitcoin-data"]  # Base de données
collection = db["prices"]  # Collection

# Initialiser Spark
spark = SparkSession.builder \
    .appName("BitcoinRealTime") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Stocker les données traitées pour l'exposer au frontend
processed_data = []


def fetch_bitcoin_data():
    # URL pour récupérer les bougies de données en temps réel
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",  # Bitcoin à USDT
        "interval": "1m",    # Intervalle de 1 minute
        "limit": 1           # Dernière bougie uniquement
    }
    
    while True:
        try:
            # Récupérer la dernière bougie
            response = requests.get(url, params=params)
            response.raise_for_status()  # Vérifier les erreurs
            
            # Traiter la bougie renvoyée par l'API
            for row in response.json():
                process_data_in_spark(row)
            
        except Exception as e:
            print(f"Error fetching data: {e}")
        
        time.sleep(10)  # Attendre 30 secondes avant la prochaine requête


def process_data_in_spark(row):
    global processed_data
    
    # Extraire les informations OHLC et le volume
    timestamp = row[0]  # Timestamp (en millisecondes)
    open_price = float(row[1])  # Prix d'ouverture
    high_price = float(row[2])  # Prix le plus élevé
    low_price = float(row[3])   # Prix le plus bas
    close_price = float(row[4]) # Prix de clôture
    volume = float(row[5])      # Volume de transactions
    
    from datetime import datetime
    time = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')  # Convertir en format lisible

    # Créer une structure de données compatible Spark
    data = [(time, open_price, high_price, low_price, close_price, volume)]
    
    # Définir le schéma des données
    schema = "time STRING, open_price FLOAT, high_price FLOAT, low_price FLOAT, close_price FLOAT, volume FLOAT"
    
    # Créer un DataFrame Spark
    df = spark.createDataFrame(data, schema=schema)

    # Collecter les données traitées
    result = df.collect()
    for r in result:
        # Ajouter les données dans la liste exposée à l'API Flask
        processed_data.append({
            "time": r["time"],
            "open_price": r["open_price"],
            "high_price": r["high_price"],
            "low_price": r["low_price"],
            "close_price": r["close_price"],
            "volume": r["volume"]
        })

        # Insérer les données dans MongoDB
        collection.insert_one({
            "time": r["time"],
            "open_price": r["open_price"],
            "high_price": r["high_price"],
            "low_price": r["low_price"],
            "close_price": r["close_price"],
            "volume": r["volume"]
        })


@app.route('/data', methods=['GET'])
def get_data():
    # Renvoyer les 20 dernières entrées pour le frontend
    return jsonify(processed_data[-20:])  


if __name__ == "__main__":
    import threading
    # Lancer le fetch des données dans un thread séparé
    threading.Thread(target=fetch_bitcoin_data).start()
    app.run(host='0.0.0.0', port=5000)
