import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


uri = "mongodb+srv://utafaro:BiSjjiYSm1THEKKl@cluster0.l71ap.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri)
db = client['bitcoin-data']
collection = db['bitcoin-batch']


data = collection.find()
df = pd.DataFrame(list(data))

df = df[['open', 'high', 'low', 'variation_percentage', 'close']]  


df.dropna(inplace=True)  


X = df[['open', 'high', 'low']] 
y = df['close']  


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


mae = mean_absolute_error(y_test, y_pred)  
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")



for i in range(10): 
    print(f"real : {y_test.iloc[i]}, predict : {y_pred[i]}")

