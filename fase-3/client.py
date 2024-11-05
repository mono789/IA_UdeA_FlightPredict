import requests

url = 'http://localhost:5001/train'
files = {'file': open('train_df.csv', 'rb')}
response = requests.post(url, files=files)
print(response.json())

url = 'http://localhost:5001/predict'
files = {'file': open('test_df.csv', 'rb')}
response = requests.post(url, files=files)
print(response.json())

