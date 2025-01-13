# Utiliser l'image officielle de Spark avec Hadoop et Python
FROM apache/spark:3.4.0

# Installer Python et pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install pyspark

# Créer un répertoire /app dans le conteneur
WORKDIR /app

# Copier ton script Python et tes fichiers de données dans le conteneur
COPY processebitcoin.py /app/
COPY entry.json /app/

# Exécuter le script Python
CMD ["python3", "processebitcoin.py"]
