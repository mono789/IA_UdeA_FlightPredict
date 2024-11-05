import argparse # Importa la librería para manejar argumentos de línea de comandos
import pickle # Para cargar y guardar objetos serializados
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report # Para medir la precisión y generar reportes de clasificación

# Función para crear y preparar el dataframe a partir de los datos originales
def create_df(df):
    # Selecciona las columnas necesarias para el análisis y predicción
    df2 = df[['SCHEDULED_DEPARTURE','SCHEDULED_ARRIVAL',
                'ORIGIN_AIRPORT','DESTINATION_AIRPORT','DEPARTURE_DELAY','AIRLINE']]
    # Elimina cualquier fila que contenga valores nulos para no quitarle valor al modelo
    df2.dropna(how='any', inplace=True)

    # Convierte las columnas de fecha y hora a tipos de datos datetime y time
    df2['SCHEDULED_DEPARTURE'] = pd.to_datetime(df2['SCHEDULED_DEPARTURE'], format="%d/%m/%Y %H:%M", dayfirst=True, errors='coerce')
    df2['SCHEDULED_ARRIVAL'] = pd.to_datetime(df2['SCHEDULED_ARRIVAL'], format='%H:%M:%S').dt.time  # Convierte a objeto de tiempo

    # Extrae el día de la semana de la columna SCHEDULED_DEPARTURE
    df2['weekday'] = df2['SCHEDULED_DEPARTURE'].dt.weekday

    # Crea una nueva columna para clasificar los vuelos en retrasados (1) o no retrasados (0)
    df2['DELAY_CLASS'] = df2['DEPARTURE_DELAY'].apply(lambda x: 1 if x >= 15 else 0)

    # Convierte las horas de salida y llegada a segundos para facilitar el modelado
    fct = lambda x: x.hour*3600 + x.minute*60 + x.second
    df2['heure_depart'] = df2['SCHEDULED_DEPARTURE'].apply(lambda x: fct(x.time()) if isinstance(x, pd.Timestamp) else fct(x))
    df2['heure_arrivee'] = df2['SCHEDULED_ARRIVAL'].apply(lambda x: fct(x.time()) if isinstance(x, pd.Timestamp) else fct(x))

    return df2


# Configura el parser de argumentos para aceptar los archivos de entrada (CSV) y el modelo (pkl)
parser = argparse.ArgumentParser(description="Realizar predicciones usando un modelo CatBoost entrenado.")
parser.add_argument("csv_file", type=str, help="Ruta al archivo CSV con los datos de entrada para predecir")
parser.add_argument("model_file", type=str, help="Ruta al archivo del modelo entrenado (.pkl)")

# Lee los argumentos de línea de comandos proporcionados por el usuario
args = parser.parse_args()

# Carga el archivo CSV con los datos de entrada
df_input = pd.read_csv(args.csv_file)
# Llama a la función create_df para procesar el dataframe
df3 = create_df(df_input)

# Carga los label encoders y el one-hot encoder desde archivos serializados (pickle)
with open('label_encoder_airport.pkl', 'rb') as f:
    label_encoder_airport = pickle.load(f)
with open('label_encoder_airline.pkl', 'rb') as f:
    label_encoder_airline = pickle.load(f)
with open('onehot_encoder_airport.pkl', 'rb') as f:
    onehot_encoder_airport = pickle.load(f)
# Carga el modelo entrenado desde el archivo .pkl
with open(args.model_file, 'rb') as f:
    model = pickle.load(f)

# Aplica el label encoding a las columnas de aeropuerto de origen y aerolínea
df3['ORIGIN_AIRPORT_ENC'] = label_encoder_airport.transform(df3['ORIGIN_AIRPORT'])
df3['AIRLINE_ENC'] = label_encoder_airline.transform(df3['AIRLINE'])

# Aplica el one-hot encoding al aeropuerto de origen
airport_encoded = onehot_encoder_airport.transform(df3[['ORIGIN_AIRPORT_ENC']])

# Crea la matriz de características (X) combinando las columnas codificadas y las horas en segundos
X = np.hstack((airport_encoded, df3[['heure_depart', 'heure_arrivee', 'weekday']].values))

# Realiza predicciones usando el modelo cargado
predictions = model.predict(X)

# Agrega las predicciones al dataframe original
df3['Prediccion_Retraso'] = predictions

# Guarda las predicciones en un archivo CSV
output_file = "predicciones_aerolineas.csv"
df3.to_csv(output_file, index=False)

print(f"\nPredicciones guardadas en {output_file}")

# Compara las predicciones con las etiquetas reales para evaluar el rendimiento
y_test = df3['DELAY_CLASS'] 
y_pred = predictions

# Calcula y muestra la precisión (accuracy)
accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy:", accuracy)

# Genera y muestra un reporte de clasificación (precisión, recall, F1-score)
print("\nClassification Report:")
print(f"\n{classification_report(y_test, y_pred)}")
