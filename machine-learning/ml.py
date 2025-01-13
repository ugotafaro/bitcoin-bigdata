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


df = df[['close']]  
df.dropna(inplace=True)


n_lags = 7  
for i in range(1, n_lags + 1):
    df[f'lag_{i}'] = df['close'].shift(i)


df.dropna(inplace=True)


X = df[[f'lag_{i}' for i in range(1, n_lags + 1)]]
y = df['close']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)


model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")

for i in range(10):
    print(f"Real: {y_test.iloc[i]}, Predicted: {y_pred[i]}")
