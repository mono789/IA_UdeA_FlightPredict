import requests

#Envía una solicitud POST al endpoint de entrenamiento con un archivo CSV para entrenar el modelo.
url = 'http://localhost:5001/train'
files = {'file': open('train_df.csv', 'rb')}
response = requests.post(url, files=files)
print(response.json())

#Envía una solicitud POST al endpoint de predicción con un archivo CSV con datos a predecir.
url = 'http://localhost:5001/predict'
files = {'file': open('test_df.csv', 'rb')}
response = requests.post(url, files=files)
print(response.json())

