# ✈️ IA_UdeA_FlightPredict

This project focuses on the analysis and prediction of flight delays using historical data from various airlines during 2015. The goal is to understand the factors that influence delays, such as the origin airport, the airline, and the interactions between origin and destination airports, to improve prediction accuracy and propose solutions to anticipate these issues.

### 👥 Team Members:
- **Kevin Estrada Del Valle** - 1036689216 - Systems Engineering Student
- **Juan Andrés Rivera Arango** - 1037666069 - Systems Engineering Student

---

## 🚀 Running the Phase-1 File

This directory contains a Jupyter Notebook file (`.ipynb`) corresponding to phase-1 of the project. Below are the steps to run the file.

### 1. Google Colab

**Steps:**

1. Go to [Google Colab](https://colab.research.google.com/).
2. In the upper right corner, click **"Open notebook"**.
3. Select the **GitHub** option.
4. Enter the URL of this repository.
5. Open the `.ipynb` file corresponding to phase-1.
6. Click **"Run"** to execute the notebook cells.

### 2. Jupyter Notebook on Your Local Environment

**Steps:**

1. Make sure you have Python and Jupyter installed on your system.
2. Clone this repository with the following command:

    ```bash
    git clone https://github.com/KevEstr/IA_UdeA_FlightPredict/tree/main
    ```

3. Navigate to the repository folder and open the notebook:

    ```bash
    cd IA_UdeA_FlightPredict
    jupyter notebook
    ```

4. Run each cell of the notebook.

---

## 🛠️ Phase-2: Model Training and Prediction

In phase-2, we focus on training a model to predict flight delays based on the historical dataset. Docker is used to containerize the environment, ensuring consistency across different systems. Below are the detailed steps to build the Docker image, train the model, and make predictions.

### 🐳 Docker Setup and Model Training

To run the training and prediction in phase-2, we use Docker to containerize the environment. This ensures that all necessary dependencies and the execution environment are standardized. Follow these steps:

### 1. Building the Docker Image

First, you need to create a Docker image based on the `Dockerfile` located in the project folder.

**Steps:**

1. Open a terminal and navigate to the project folder where the `Dockerfile` is located (in this case, the root of fase-2)
2. Build the Docker image using the following command:

    ```bash
    docker build -t fase_2 .
    ```

   This command creates an image named `fase_2` based on the `Dockerfile`. The image contains all the necessary dependencies for training and running the model.

### 2. Training the Model

Once the Docker image is built, you can train the model using the provided training dataset (`train_df.csv`).

**Steps:**

1. In the terminal, navigate to the root of the project and run the following command to train the model:

    ```bash
    docker run -it -v ${PWD}:/app fase_2 python train.py train_df.csv
    ```

   - `-it`: Runs Docker interactively.
   - `-v ${PWD}:/app`: Mounts the current working directory into the Docker container at `/app`.
   - `fase_2`: The name of the Docker image.
   - `python train.py train_df.csv`: Executes the training script, `train.py`, using the `train_df.csv` file as input.

   This command will train the model and save the resulting trained model (`modelo_entrenado.pkl`) in the current directory.

### 3. Making Predictions

After training the model, you can use it to make predictions. You will need the airline code (`codigo_aerolinea`) and the trained model file (`modelo_entrenado.pkl`).

The **airline code** refers to the abbreviation for each airline that we used to train the model. Since the idea is to predict the delay time for a specific airline, this abbreviation is required as input.

Additionally, a clean `train.csv` file is required as part of the phase 2 process, where the corresponding predictions will be made. Ensure that the dataset adheres to the expected structure for the model. The required columns are as follows:

- `AIRLINE`
- `ORIGIN_AIRPORT`
- `DESTINATION_AIRPORT`
- `SCHEDULED_DEPARTURE`
- `DEPARTURE_TIME`
- `DEPARTURE_DELAY`
- `SCHEDULED_ARRIVAL`
- `ARRIVAL_TIME`
- `ARRIVAL_DELAY`
- `SCHEDULED_TIME`
- `ELAPSED_TIME`

**Steps:**

1. In the terminal, navigate to the project folder and run the following command to make predictions:

    ```bash
    docker run -it -v ${PWD}:/app fase_2 python predict.py train_df.csv codigo_aerolinea modelo_entrenado.pkl
    ```

   - `train_df.csv`: The dataset used to make predictions.
   - `codigo_aerolinea`: Replace this with the actual airline code for which you want to predict delays.
   - `modelo_entrenado.pkl`: The trained model file generated during the training phase.

   This command will output the predicted delays based on the input airline code and the trained model.

---

### 📝 Summary of What’s Happening

- **Docker Image Creation:** We create a Docker image to ensure all dependencies are installed and the environment is consistent across systems.
- **Model Training:** The `train.py` script is used to train a machine learning model based on the provided dataset (`train_df.csv`). The resulting trained model is saved as `modelo_entrenado.pkl`.
- **Prediction:** The `predict.py` script is used to predict flight delays for a given airline, based on the trained model and the dataset.

These steps ensure a smooth and consistent environment for training the model and making predictions. The output of the predictions can be used to anticipate flight delays and propose operational improvements.
