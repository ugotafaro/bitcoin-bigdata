import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 1. Connexion à MongoDB et récupération des données
uri = "mongodb+srv://utafaro:BiSjjiYSm1THEKKl@cluster0.l71ap.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri)
db = client['bitcoin-data']
collection = db['bitcoin-batch']

# 2. Récupérer les données de MongoDB
data = collection.find()
df = pd.DataFrame(list(data))

# 3. Préparation des données
# Filtrer et renommer les colonnes pour faciliter la manipulation
df = df[['open', 'high', 'low', 'variation_percentage', 'close']]  # Garder les colonnes nécessaires

# Vérifier s'il y a des valeurs nulles et les gérer
df.dropna(inplace=True)  # Supprimer les lignes avec des valeurs manquantes

# Sélectionner les caractéristiques (features) et la cible (target)
X = df[['open', 'high', 'low']]  # Caractéristiques
y = df['close']  # Cible : prix de fermeture (close)

# Diviser les données en ensembles d'entraînement et de test (80% pour l'entraînement et 20% pour le test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entraînement du modèle de régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Prédictions et évaluation
y_pred = model.predict(X_test)

# 6. Affichage des résultats
# Afficher les performances du modèle
mae = mean_absolute_error(y_test, y_pred)  # Erreur absolue moyenne
mse = mean_squared_error(y_test, y_pred)  # Erreur quadratique moyenne

print(f"Mean Absolute Error (MAE): {mae}")


# Optionnel : afficher quelques prédictions comparées aux vraies valeurs
for i in range(10):  # Afficher les 10 premières prédictions
    print(f"real : {y_test.iloc[i]}, predict : {y_pred[i]}")

