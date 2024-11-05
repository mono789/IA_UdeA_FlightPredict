# Usar una imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos del directorio actual al directorio de trabajo en el contenedor
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install Flask loguru numpy

CMD flask --app apirest run --host=0.0.0.0 