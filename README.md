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
    git clone https://github.com/KevEstr/IA_UdeA_FlightPredict
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

1. Open a terminal and navigate to the project folder where the `Dockerfile` is located (in this case, the root of fase-2) using the `cd` command:
    
    ```bash
       cd fase-2
    ```

2. Build the Docker image using the following command:

    ```bash
    docker build -t fase_2 .
    ```

   This command creates an image named `fase_2` based on the `Dockerfile`. The image contains all the necessary dependencies for training and running the model.

To run this project, you must have the following files in the project directory:

1. **`train_df.csv`** - The dataset used for training the model. This file contains historical data on flight delays.
2. **`test_df.csv`** - The dataset used for making predictions. Ensure it follows the structure required by the model for accurate predictions.

Both files should contain the necessary columns as described in the project documentation, and be placed in the project folder before running the training and prediction scripts.

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

After training the model, you can use it to make predictions. 

As mentioned earlier, a `train.csv` file is required as part of the phase 2 process, where the corresponding predictions will be made. Ensure that the dataset adheres to the expected structure for the model. The required columns are as follows:

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

In any case, there is an example within the folder that shows the structure to follow for constructing the `train.csv` file.

**Steps:**

1. In the terminal, navigate to the project folder and run the following command to make predictions:

    ```bash
    docker run -it -v ${PWD}:/app fase_2 python predict.py train_df.csv modelo_entrenado.pkl
    ```

   - `train_df.csv`: The dataset used to make predictions.
   - `modelo_entrenado.pkl`: The trained model file generated during the training phase.

   This command will output the predicted delays based on the input airline code and the trained model.

---

### [OPTIONAL] Running the Project with `run-scripts.ipynb`

As an alternative, we have created a centralized script file called `run-scripts.ipynb`. This file consolidates all the necessary steps and commands for the project into one place, allowing you to execute everything without needing to run multiple scripts individually.

**Steps:**

1. Open the `run-scripts.ipynb` file located in the project directory.
2. Execute each section of the file sequentially to perform the entire process, from training the model to making predictions, without having to run each script separately.

This provides a streamlined approach to manage the project from start to finish.

---
### 📝 Summary of What’s Happening

- **Docker Image Creation:** We create a Docker image to ensure all dependencies are installed and the environment is consistent across systems.
- **Model Training:** The `train.py` script is used to train a model based on the provided dataset (`train_df.csv`). The resulting trained model is saved as `modelo_entrenado.pkl`.
- **Prediction:** The `predict.py` script is used to predict flight delays for a given airline, based on the trained model and the dataset.

These steps ensure a smooth and consistent environment for training the model and making predictions. The output of the predictions can be used to anticipate flight delays and propose operational improvements.

---
## 🖥️ Phase-3: REST API for Flight Delay Prediction

In Phase-3, we extend the project by creating a RESTful API to expose the flight delay prediction model as a service. This enables users or other applications to make HTTP requests to predict flight delays based on input parameters, streamlining access to the model's predictions. The API is built using Flask and is containerized using Docker to maintain consistency in deployment across various environments.

This phase includes two primary files:

- **`apirest.py`**: The REST API server.
- **`client.py`**: A client script for testing and interacting with the API.

The API exposes two main endpoints:

- **`POST /predict:`** For predicting delays based on flight information.
- **`POST /train:`** For retraining the model with new or updated data.

### Overview of the API

The REST API serves as a wrapper for the trained model, enabling users to send POST requests with flight data to obtain predictions. It exposes one main endpoint that accepts flight data and responds with predicted delay times.

### Setting Up the API with Docker
Follow these steps to build and run the API server in a Docker container.

1. **Build the Docker Image**:
    1. Ensure you are in the project directory containing the Dockerfile.
        ```bash
        cd fase-3
        ``` 
    2. Run the following command to build the Docker image:
     
        ```bash
        docker build -t fase_3 .
        ``` 
        This command creates a Docker image named fase_3 with all necessary dependencies for the API. 
2. **Running the API Server:**
    1. After building the Docker image, start the API server using:

        ```bash
        docker run -it -p 5001:5000 fase_3
        ```
        This command runs apirest.py, the API server file, on port 5000.

### API Endpoint Details
The REST API provides the following endpoint:

### `POST /train:`
**Description:** Retrains the model with a new dataset provided in CSV format.

**Method:** POST

**Input Format:** Multipart form data, with the CSV file containing the training data.

**Required File:** A CSV file (train_df.csv) containing updated or new training data. It should have the same structure as the original training dataset. Ensure it follows the structure required by the model for accurate training.

### `POST /predict:`
**Description:** This endpoint accepts flight data and returns a prediction on the delay.

**Method:** POST

**Input Format:** Multipart form data, with the CSV file containing the predicting data.

**Required File:** A CSV file (test_df.csv) containing new testing data. It should have the same structure as the original training dataset. Ensure it follows the structure required by the model for accurate predictions.

## Testing the API with client.py
The client.py script simplifies interaction with the API by sending requests to both the /predict and /train endpoints with appropriate data formats.

1. **Running Predictions:**
To make a prediction, `client.py` sends a request to `/predict `with sample flight data and prints the predicted delay.

2. **Retraining the Model:** To retrain the model, `client.py` can also be configured to send a CSV file to the `/train` endpoint.

Run `client.py` on a separate shell to interact with the API endpoints:

```bash
python client.py
```

### 📝Summary of Phase-3
1. **Containerization:** The API is encapsulated in a Docker container for consistent deployment.
2. **Predictive Service:** The /predict endpoint uses the trained model to provide delay predictions based on real-time flight data.
3. **Retraining Functionality:** The /train endpoint enables dynamic retraining of the model with updated data.
4. **Ease of Use:** The client.py script enables easy testing and interaction with both endpoints.

This phase makes the predictive model accessible to external applications or services and enables continual model updates with fresh data.
    
