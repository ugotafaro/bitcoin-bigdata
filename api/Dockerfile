FROM bitnami/spark:latest

# Installer Python et les dépendances nécessaires
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean

# Définir JAVA_HOME (il est déjà configuré dans cette image)
ENV PATH="/opt/bitnami/spark/bin:/opt/bitnami/java/bin:$PATH"

WORKDIR /app
COPY . .

# Installer les dépendances Python
RUN pip3 install pyspark requests flask flask-cors pymongo python-dotenv flask_socketio gunicorn


FROM bitnami/spark:latest

# Installer Python et les dépendances nécessaires
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean

# Définir JAVA_HOME (il est déjà configuré dans cette image)
ENV PATH="/opt/bitnami/spark/bin:/opt/bitnami/java/bin:$PATH"

WORKDIR /app
COPY . .

# Installer les dépendances Python
RUN pip3 install pyspark requests flask flask-cors pymongo python-dotenv 

# Utiliser Gunicorn pour exécuter l'application Flask
CMD ["python", "app.py"]    
