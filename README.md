# 🎾🔮 AceBet: Tennis Match Predictor (Mock-up)

**Please note:** This document describes a mock-up version of AceBet. While it showcases the concept and functionality, it is not intended for production use.

Welcome to AceBet, your playful playground for peeking into the future of tennis matches!

![Tennis Match](tennis-unsplash.jpg)

## Table of Contents

- [🎾🔮 AceBet: Tennis Match Predictor (Mock-up)](#-acebet-tennis-match-predictor-mock-up)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Getting Started](#getting-started)
  - [API Endpoints](#api-endpoints)
  - [Authentication Magic](#authentication-magic)
  - [Prediction](#prediction)
  - [AceBet-in-action](#acebet-in-action)
  - [From Mock-up to Production](#from-mock-up-to-production)
  - [Conclusion](#conclusion)
  - [Project structure](#project-structure)
  - [Database preparation](#database-preparation)
  - [Training procedure](#training-procedure)
  - [Predict procedure](#predict-procedure)

## Introduction

Ever wondered if you could predict tennis match outcomes before the first serve? Enter our brainchild, AceBet! This report spills the beans on the concept, its whiz-bang features, and what lies ahead as we aim to take it from fantasy to reality.

AceBet is a web-based application built using the FastAPI framework. It harnesses the power of machine learning to predict tennis match outcomes, including both the probability and the class of the outcome. The system incorporates user authentication for access control and offers endpoints for user interactions.

## Getting Started

1. Install the FastAPI library and dependencies with `pip install fastapi uvicorn[standard]`.
2. Fire up your crystal ball by running `uvicorn main:app --reload`.

## API Endpoints

Our AceBet has some exciting booths to visit:

- **/token**: This endpoint facilitates user authentication, issuing access tokens for secure interactions.
- **/users/me/**: It offers users access to their individual profiles, presenting user-specific information.
- **/users/me/items/**: This endpoint grants access to personalized collections of items associated with the user.
- **/predict/**: Users can utilize this endpoint to submit match prediction requests, supplying player names and match date.

## Authentication Magic

AceBet isn't open to just anyone. To access its secrets, you need an access token. Visit the `/token` booth, share your credentials, and get your magical token for AceBet.

## Prediction

The `/predict` booth is where the real magic happens. Provide player names and a match date, and AceBet's enchanted algorithms will predict the match outcome! You'll get the player's name, the probability of their victory, and the predicted class (0 or 1).

## AceBet-in-action

Initiating a match prediction involves sending a POST request, as depicted:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "p1_name": "Nadal",
  "p2_name": "Federer",
  "date": "2023-06-30"
}'
```

You'll receive predictions like:
```json
{
  "player_name": "Nadal",
  "prob": 73.5,
  "class_": 1
}
```

## From Mock-up to Production

While AceBet is currently a mock-up, it's just the tip of the iceberg. The journey from mock-up to production involves:

1. **Refining the Models**: Enhance the predictive models with more data, fine-tuning, and advanced algorithms to improve accuracy.
2. **Scalability and Optimization**: Optimize the code for scalability, ensuring smooth performance even with high user loads.
3. **Security Enhancements**: Fortify the app with robust security measures to protect user data and ensure safe interactions.
4. **UI/UX Transformation**: Elevate the user experience with an engaging interface and intuitive interactions.
5. **Deployment and Monitoring**: Deploy the app on a production server, and set up monitoring to keep an eye on its health and performance.
6. **Continuous Improvement**: Regularly update and improve the app based on user feedback and changing requirements.

## Conclusion

AceBet, in its mock-up form, promises a glimpse into the world of match predictions. As we journey from mock-up to production, we're excited to transform it into a powerful tool that offers accurate predictions and an enchanting user experience. Stay tuned for more magical updates! 🎾🔮

## Project structure

```
Sports_betting/
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── model_training.ipynb
│   └── ...
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── ...
│   ├── models/
│   │   ├── model.py
│   │   └── ...
│   ├── utils/
│   │   ├── data_processing.py
│   │   └── ...
│   ├── tests/
│   │   ├── test_api.py
│   │   └── ...
│   ├── main.py
│   └── ...
├── data/
│   ├── dataset.csv
│   └── ...
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── ...
├── requirements.txt
├── README.md
└── ...
```

 * notebooks/: Jupyter notebooks for data exploration, model training, and any other exploratory or experimental analyses. For pre-production steps.
 * src/: This folder holds the main source code .
     - api/: API-related files, including the main FastAPI file (main.py) and any additional files for defining API routes, request/response models, and authentication.
     - models/: Files related to machine learning models, such as model definitions (model.py), model training scripts, and any utilities specific to the models.
     - utils/: Utility functions or modules that provide common functionalities used across the project, such as data preprocessing, feature engineering, or custom metrics. It could be replaced by a python package.
     - tests/: Test files, such as unit tests for the API endpoints or model evaluation.
     - main.py: The main entry point of your application.
 * data/: Dataset and any other relevant data files required for training and testing your models. To be excluded from versioning (gitignore).
 * docker/: Docker-related files.
     - Dockerfile: The Dockerfile specifies the environment and dependencies required to run the application. It defines the steps to build a Docker image.
     - docker-compose.yml: If we have multiple containers or services to run (e.g., the API, database), docker-compose.yml file to define and manage the composition of these services.
 * requirements.txt: Python dependencies required for your project, to install the necessary packages using pip. It could be a conda yaml.
 * README.md: A markdown file where you can provide a brief description of the project, installation instructions, usage guidelines, and any other relevant information. It could be broken down into CHANGELOG, etc.


## Database preparation

The `dataprep.py` efficiently prepares ATP (Association of Tennis Professionals) data for predictive modeling. It starts by loading structured data into a DataFrame, then standardizes dates and reorganizes columns to align with modeling needs. It introduces practical feature enhancements, such as year, month, day, and rank difference. Swapping player columns ensures logical coherence. Finally, the processed data is stored for future use. This process establishes a solid foundation for subsequent predictive analysis in the realm of tennis match outcomes.
## Training procedure

The `train.py` segment presented orchestrates the process of training a machine learning model (ligthgbm) for AceBet Match Predictor. The pipeline commences with data preparation, where a specific time window is extracted from the ATP dataset, ranging from the `start_date` to the `end_date`. Features are then selected, excluding certain columns irrelevant to the task. This preprocessed data is subject to a `TimeSeriesSplit`, creating a division into training and test sets, with the former primarily utilized for model training.

The LightGBM classifier is used for predictive modeling (best, fastest and less prone to overfitting model, see the `atp_tennis.ipynb`), integrated within a pipeline along with an Ordinal Encoder to handle categorical variables. The model is trained on the training dataset, and upon completion, the pipeline is serialized and saved as a joblib file. This allows for easy model preservation and future utilization. Notably, the model's parameters are finely tuned for optimal performance, an essential aspect of the model's efficacy.

Though presented in a prototype phase, this segment encapsulates the essence of AceBet's machine learning engine. As the application progresses towards production, further refinements and optimizations are anticipated to enhance the model's predictive prowess, contributing to the project's ultimate goal of accurate match outcome prediction.

## Predict procedure

The `predict_winner.py` segment of code orchestrates the prediction process for a given match outcome after model training. First, loading the data from a Feather file, ensuring compatibility with the previous training data. The data is queried to extract relevant details for the specific players and match date.

Loading the latest trained model, the prediction function estimates the probability of Player 1 winning the match. The function returns the winning probability, the class prediction (0 or 1), and the name of Player 1. To facilitate the prediction process..

The model loading is executed through the `load_model` function, extracting the most recent model stored within a specified directory. Subsequently, the `make_prediction` function orchestrates the entire prediction procedure, from data loading to querying and prediction.

When executed independently, this segment demonstrates the prediction process for a specific match scenario. A test case is provided as a prototype, encapsulating the envisioned application's functionality. The printed result offers insights into Player 1's winning probability, a key facet of AceBet's capabilities. As the project advances towards production, further optimizations and scalability considerations are anticipated to enhance the prediction engine's accuracy and reliability.
