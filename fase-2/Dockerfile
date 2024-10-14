# Usar una imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos del directorio actual al directorio de trabajo en el contenedor
COPY . /app

# Instalar las dependencias listadas en el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Especificar el comando por defecto para ejecutar el script de predicción
CMD ["python", "predict.py"]
