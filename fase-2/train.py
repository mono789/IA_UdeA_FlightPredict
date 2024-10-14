from catboost import CatBoostClassifier # Importa el clasificador CatBoost
from sklearn.preprocessing import LabelEncoder, OneHotEncoder # Para codificar variables categóricas
from sklearn.metrics import accuracy_score, classification_report # Para evaluar el rendimiento del modelo
from sklearn.model_selection import train_test_split # Para dividir los datos en entrenamiento y prueba
import pickle  # Para serializar el modelo entrenado y otros objetos
import sys  # Para manejar argumentos de línea de comandos
import numpy as np
import pandas as pd
import argparse

# Función para crear y procesar el dataframe con las características y el objetivo
def create_df(df):
    # Filtra el dataframe para seleccionar solo las columnas relevantes
    df2 = df[['SCHEDULED_DEPARTURE','SCHEDULED_ARRIVAL',
                'ORIGIN_AIRPORT','DESTINATION_AIRPORT','DEPARTURE_DELAY','AIRLINE']]
    df2.dropna(how='any', inplace=True)

    # Convierte las columnas de fecha y hora en objetos datetime
    df2['SCHEDULED_DEPARTURE'] = pd.to_datetime(df2['SCHEDULED_DEPARTURE'], format="%d/%m/%Y %H:%M", dayfirst=True,)    
    df2['SCHEDULED_ARRIVAL'] = pd.to_datetime(df2['SCHEDULED_ARRIVAL'], format='%H:%M:%S').dt.time  # Convierte a objeto de tiempo

    # Añade una columna que indica el día de la semana (lunes=0, domingo=6)
    df2['weekday'] = df2['SCHEDULED_DEPARTURE'].apply(lambda x: x.weekday())

    # Clasificación binaria: 1 si el retraso es >= 15 minutos, 0 si no
    df2['DELAY_CLASS'] = df2['DEPARTURE_DELAY'].apply(lambda x: 1 if x >= 15 else 0)

    # Convierte las horas de salida y llegada en segundos desde la medianoche
    fct = lambda x: x.hour*3600 + x.minute*60 + x.second
    df2['heure_depart'] = df2['SCHEDULED_DEPARTURE'].apply(lambda x: fct(x.time()) if isinstance(x, pd.Timestamp) else fct(x))
    df2['heure_arrivee'] = df2['SCHEDULED_ARRIVAL'].apply(lambda x: fct(x.time()) if isinstance(x, pd.Timestamp) else fct(x))

    return df2


# Configuración de argparse para manejar la entrada del archivo CSV desde la línea de comandos
parser = argparse.ArgumentParser(description="Entrenamiento de modelo CatBoost para predicción de retrasos.")
parser.add_argument("csv_file", type=str, help="Ruta al archivo CSV con los datos de entrenamiento")

# Parsear los argumentos
args = parser.parse_args()

# Preprocesamiento del dataframe
df3 = create_df(pd.read_csv(args.csv_file))

# Codificación de la columna categórica 'ORIGIN_AIRPORT'
label_encoder_airport  = LabelEncoder()
df3['ORIGIN_AIRPORT_ENC'] = label_encoder_airport .fit_transform(df3['ORIGIN_AIRPORT'])
label_encoder_airline = LabelEncoder()
df3['AIRLINE_ENC'] = label_encoder_airline.fit_transform(df3['AIRLINE'])

# Codificación one-hot de 'ORIGIN_AIRPORT_ENC'
onehot_encoder_airport  = OneHotEncoder(sparse_output=False)
onehot_encoder_airline  = OneHotEncoder(sparse_output=False)  # Cambiado 'sparse' a 'sparse_output'
airport_encoded = onehot_encoder_airport.fit_transform(df3[['ORIGIN_AIRPORT_ENC']])
airline_encoded = onehot_encoder_airline.fit_transform(df3[['AIRLINE_ENC']])


# Preparación de los datos para el modelo
# Combina las columnas codificadas one-hot y las características adicionales (hora de salida, llegada, día de la semana)
X = np.hstack((airport_encoded, df3[['heure_depart', 'heure_arrivee', 'weekday']].values))
Y = df3['DELAY_CLASS'].values  # Usamos la columna binaria DELAY_CLASS como objetivo

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Crear el modelo CatBoostClassifier
catboost_model = CatBoostClassifier(iterations=1000, learning_rate=0.1, depth=6, verbose=100)

# Entrenar el modelo
catboost_model.fit(X_train, y_train)

# Guarda el modelo entrenado en un archivo pickle para su uso posterior
with open('modelo_entrenado.pkl', 'wb') as f:
    pickle.dump(catboost_model, f)

with open('label_encoder_airport.pkl', 'wb') as f:
    pickle.dump(label_encoder_airport, f)
with open('label_encoder_airline.pkl', 'wb') as f:
    pickle.dump(label_encoder_airline, f)
with open('onehot_encoder_airport.pkl', 'wb') as f:
    pickle.dump(onehot_encoder_airport, f)

#model_features = catboost_model.feature_names_
#print(model_features)
#print("catboost_model.feature_names_: ", catboost_model.feature_names_)
#print("COLUMNS TYPE TRAIN: ", df3.dtypes)

# Mensaje de confirmación
print("Modelo entrenado con CatBoost y guardado como modelo_entrenado.pkl")