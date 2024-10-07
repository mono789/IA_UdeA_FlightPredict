import argparse
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report

def create_df(df):
    df2 = df[['SCHEDULED_DEPARTURE','SCHEDULED_ARRIVAL',
                'ORIGIN_AIRPORT','DESTINATION_AIRPORT','DEPARTURE_DELAY','AIRLINE']]
    df2.dropna(how='any', inplace=True)
    df2['SCHEDULED_DEPARTURE'] = pd.to_datetime(df2['SCHEDULED_DEPARTURE'])
    df2['SCHEDULED_ARRIVAL'] = pd.to_datetime(df2['SCHEDULED_ARRIVAL'])
    df2['weekday'] = df2['SCHEDULED_DEPARTURE'].dt.weekday
    df2['DELAY_CLASS'] = df2['DEPARTURE_DELAY'].apply(lambda x: 1 if x >= 15 else 0)
    fct = lambda x: x.hour*3600 + x.minute*60 + x.second
    df2['heure_depart'] = df2['SCHEDULED_DEPARTURE'].dt.time.apply(fct)
    df2['heure_arrivee'] = df2['SCHEDULED_ARRIVAL'].dt.time.apply(fct)
    return df2

parser = argparse.ArgumentParser(description="Realizar predicciones usando un modelo CatBoost entrenado.")
parser.add_argument("csv_file", type=str, help="Ruta al archivo CSV con los datos de entrada para predecir")
parser.add_argument("model_file", type=str, help="Ruta al archivo del modelo entrenado (.pkl)")

args = parser.parse_args()

df_input = pd.read_csv(args.csv_file)
df3 = create_df(df_input)

with open('label_encoder_airport.pkl', 'rb') as f:
    label_encoder_airport = pickle.load(f)
with open('label_encoder_airline.pkl', 'rb') as f:
    label_encoder_airline = pickle.load(f)
with open('onehot_encoder_airport.pkl', 'rb') as f:
    onehot_encoder_airport = pickle.load(f)
with open(args.model_file, 'rb') as f:
    model = pickle.load(f)

df3['ORIGIN_AIRPORT_ENC'] = label_encoder_airport.transform(df3['ORIGIN_AIRPORT'])
df3['AIRLINE_ENC'] = label_encoder_airline.transform(df3['AIRLINE'])

airport_encoded = onehot_encoder_airport.transform(df3[['ORIGIN_AIRPORT_ENC']])
X = np.hstack((airport_encoded, df3[['heure_depart', 'heure_arrivee', 'weekday']].values))

predictions = model.predict(X)
df3['Prediccion_Retraso'] = predictions

output_file = "predicciones_todas_aerolineas.csv"
df3.to_csv(output_file, index=False)

print(f"Predicciones guardadas en {output_file}")

y_test = df3['DELAY_CLASS'] 
y_pred = predictions

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("Classification Report:")
print(classification_report(y_test, y_pred))
