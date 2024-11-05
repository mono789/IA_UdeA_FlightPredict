# Usar una imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos del directorio actual al directorio de trabajo en el contenedor
COPY . /app

# Instalar las dependencias especificadas en requirements.txt sin cache
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Flask, loguru y numpy
RUN pip install Flask loguru numpy

# Ejecutar la aplicación Flask en el host 0.0.0.0 para permitir el acceso externo
CMD flask --app apirest run --host=0.0.0.0 