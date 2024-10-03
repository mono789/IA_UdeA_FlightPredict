import argparse
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report


def create_df(df):
    # Filtrar las filas del carrier y seleccionar las columnas necesarias
    df2 = df[['SCHEDULED_DEPARTURE','SCHEDULED_ARRIVAL',
                'ORIGIN_AIRPORT','DESTINATION_AIRPORT','DEPARTURE_DELAY','AIRLINE']]
    df2.dropna(how='any')
    # Convertir las columnas de fecha a datetime
    df2.loc[:, 'SCHEDULED_DEPARTURE'] = pd.to_datetime(df2['SCHEDULED_DEPARTURE'])
    df2['SCHEDULED_ARRIVAL'] = pd.to_datetime(df2['SCHEDULED_ARRIVAL'])

    # Añadir columna con el día de la semana
    df2['weekday'] = df2['SCHEDULED_DEPARTURE'].apply(lambda x: x.weekday())

    # Convertir retrasos en una clasificación binaria (0: no retraso, 1: retraso >= 15 minutos)
    df2['DELAY_CLASS'] = df2['DEPARTURE_DELAY'].apply(lambda x: 1 if x >= 15 else 0)

    # Convertir las horas a segundos
    fct = lambda x: x.hour*3600 + x.minute*60 + x.second
    df2['heure_depart'] = df2['SCHEDULED_DEPARTURE'].apply(lambda x: fct(x.time()) if isinstance(x, pd.Timestamp) else None)
    df2['heure_arrivee'] = df2['SCHEDULED_ARRIVAL'].apply(lambda x: fct(x.time()) if isinstance(x, pd.Timestamp) else None)

    return df2

# Configurar argparse para recibir el archivo CSV y el carrier
parser = argparse.ArgumentParser(description="Realizar predicciones usando un modelo CatBoost entrenado.")
parser.add_argument("csv_file", type=str, help="Ruta al archivo CSV con los datos de entrada para predecir")
parser.add_argument("carrier", type=str, help="Código de la aerolínea a filtrar (ejemplo: UA, DL, etc.)")
parser.add_argument("model_file", type=str, help="Ruta al archivo del modelo entrenado (.pkl)")

# Parsear los argumentos
args = parser.parse_args()

# Cargar los datos de entrada
df_input = pd.read_csv(args.csv_file)
df_filtered = df_input[df_input['AIRLINE'] == args.carrier]

# Preprocesar el dataframe
df3 = create_df(df_filtered)


# Cargar encoders y modelo entrenado
with open('label_encoder_airport.pkl', 'rb') as f:
    label_encoder_airport = pickle.load(f)
with open('label_encoder_airline.pkl', 'rb') as f:
    label_encoder_airline = pickle.load(f)
with open('onehot_encoder_airport.pkl', 'rb') as f:
    onehot_encoder_airport = pickle.load(f)
with open(args.model_file, 'rb') as f:
    model = pickle.load(f)


# Codificación de la columna categórica 'ORIGIN_AIRPORT'
#label_encoder = LabelEncoder()

# Validar si la aerolínea especificada está en el LabelEncoder entrenado
if args.carrier not in label_encoder_airline.classes_:
    raise ValueError(f"La aerolínea {args.carrier} no está en el conjunto de datos de entrenamiento.")


df3['ORIGIN_AIRPORT_ENC'] = label_encoder_airport.transform(df3['ORIGIN_AIRPORT'])
df3['AIRLINE_ENC'] = label_encoder_airline.transform(df3['AIRLINE'])

# Codificación one-hot de 'ORIGIN_AIRPORT_ENC'
#onehot_encoder = OneHotEncoder(sparse_output=False)  # Cambiado 'sparse' a 'sparse_output'
airport_encoded = onehot_encoder_airport.transform(df3[['ORIGIN_AIRPORT_ENC']])

# Preparación de los datos para el modelo
X = np.hstack((airport_encoded, df3[['heure_depart', 'heure_arrivee', 'weekday']].values))

# Realizar predicciones
predictions = model.predict(X)

# Mostrar los resultados de las predicciones
df3['Prediccion_Retraso'] = predictions

# Guardar los resultados en un archivo CSV
output_file = f"predicciones_{args.carrier}.csv"
df3.to_csv(output_file, index=False)

#print("COLUMNS PREDICT: ",df3.columns)
#print("COLUMNS TYPE PREDICT: ", df3.dtypes)

print(f"Predicciones guardadas en {output_file}")

y_test = df3['DELAY_CLASS'] 
y_pred = predictions

# Calcular la precisión
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Reporte de clasificación
print("Classification Report:")
print(classification_report(y_test, y_pred))
