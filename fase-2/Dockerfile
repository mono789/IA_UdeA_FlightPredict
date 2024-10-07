# Usar una imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Especificar el comando por defecto (puedes cambiarlo según lo necesites)
CMD ["python", "predict.py"]
