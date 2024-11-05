from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Endpoint para realizar predicciones
@app.route('/predict', methods=['POST'])
def predict():
    # Verifica si se proporcionó un archivo CSV
    print("Received a request to /predict")
    if 'file' not in request.files:
        print("No file part") 
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    print("File received:", file.filename)
    if file.filename == '':
        print("No selected file") 
        return jsonify({"error": "No selected file"}), 400
    file.save('test_data.csv') # Guarda el archivo CSV en una ubicación temporal
    
    # Ejecuta el script predict.py y pasa la ruta del archivo CSV
    result = subprocess.run(
        ['python', 'predict.py', 'test_data.csv', 'modelo_entrenado.pkl'],  # Pasa la ruta del archivo CSV como argumento
        text=True,
        capture_output=True
    )
    
    # Procesa y devuelve el resultado de la predicción
    if result.returncode == 0:
        return jsonify({"prediction": result.stdout.strip()})
    else:
        return jsonify({"error": result.stderr.strip()}), 500

# Endpoint para lanzar el entrenamiento
@app.route('/train', methods=['POST'])
def train():
    print("Received a request to /train")
    if 'file' not in request.files:
        print("No file part") 
        return jsonify({"error": "No file provided"}), 400

    # Guarda el archivo CSV proporcionado en la ubicación temporal
    file = request.files['file']
    print("File received:", file.filename)
    if file.filename == '':
        print("No selected file") 
        return jsonify({"error": "No selected file"}), 400
    file.save('train_data.csv')
    
    # Ejecuta el script train.py pasando la ruta del archivo CSV
    result = subprocess.run(
        ['python', 'train.py', 'train_data.csv'],
        capture_output=True,
        text=True
    )
    # Procesa el resultado del entrenamiento
    if result.returncode == 0:
        return jsonify({"status": "Training completed successfully"})
    else:
        return jsonify({"error": result.stderr.strip()}), 500

if __name__ == '__main__':
    # Ejecuta la aplicación Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
