from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import os

# Lister les fichiers disponibles dans le répertoire monté (/app)
print("Fichiers disponibles dans /app :")
print(os.listdir("/app"))

# Créer une session Spark
spark = SparkSession.builder \
    .appName("Bitcoin Processing") \
    .getOrCreate()

# Lire le fichier JSON avec les options de gestion des erreurs
df = spark.read.option("mode", "DROPMALFORMED").option("multiLine", "true").json("/app/entry.json")

# Vérifier le schéma du DataFrame
df.printSchema()

# Afficher les premières lignes du DataFrame pour vérifier que les données sont bien chargées
df.show(truncate=False)

# Convertir les colonnes en Float après avoir vérifié que les données sont bien présentes
df = df.withColumn("open", F.col("open").cast("float")) \
       .withColumn("high", F.col("high").cast("float")) \
       .withColumn("low", F.col("low").cast("float")) \
       .withColumn("close", F.col("close").cast("float"))

# Vérifier les données après la conversion en float
print("Données chargées et converties :")
df.show()

# Vérifier si le DataFrame n'est pas vide avant de procéder aux calculs
if df.head(1):  # Si des données existent
    # Calcul de la variation en pourcentage par rapport au jour précédent
    window_spec = Window.orderBy("date")
    df = df.withColumn("previous_close", F.lag("close").over(window_spec))
    df = df.withColumn("variation_percentage", 
                       (F.col("close") - F.col("previous_close")) / F.col("previous_close") * 100)

    # Calcul de la tendance (True si la variation est positive)
    df = df.withColumn("tendance", F.when(F.col("variation_percentage") > 0, True).otherwise(False))

    # Afficher les résultats
    print("Données traitées :")
    df.show()

    # Sauvegarder les résultats dans un fichier JSON en écrasant l'ancien fichier
df.select("date", "open", "close", "low", "high", "variation_percentage", "tendance") \
    .write.mode("overwrite").json("/app/processed_bitcoin_data2.json")
print("Fichier JSON écrit avec succès.")