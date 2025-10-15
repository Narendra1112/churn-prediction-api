Customer Churn Prediction with Real-Time Monitoring
Overview

Customer churn refers to the rate at which customers stop doing business with a company.
High churn rates often signal dissatisfaction, pricing issues, or strong competition.
Accurately predicting which customers are likely to leave helps companies take proactive steps—like offering incentives, improving service quality, or redesigning plans—to retain valuable clients.

This project builds an end-to-end churn prediction system powered by FastAPI for backend inference, Streamlit for visualization, and real-time monitoring using Prometheus and Grafana.

Deployment

Deployed as an interactive web application with monitoring support.

Streamlit App: localhost:8501

FastAPI Docs: localhost:8000/docs

Prometheus: localhost:9090

Grafana Dashboard: localhost:3000

(You can deploy the API to Render — free cloud hosting for demo purposes.)

Objective

Build a machine learning model to predict the probability of customer churn.

Integrate the trained model into a real-time FastAPI service.

Create a Streamlit UI for easy input and visualization.

Add Prometheus + Grafana to track API latency, inference speed, and churn distribution in real time.

Demonstrate full MLOps-style observability for production-ready ML applications.

Dataset

The dataset is derived from the IBM Telco Customer Churn Dataset
.
It includes customer demographics, account information, services subscribed, and churn history.

Key categories:

Demographics: gender, senior citizen, partner, dependents

Account: tenure, contract type, payment method, paperless billing

Services: phone, internet, tech support, online backup, streaming services

Target: Churn (Yes / No)

Exploratory Data Analysis (EDA)

Correlation of features with churn


Feature Importance from XGBoost


Model Used

Logistic Regression

Random Forest

Gradient Boosting

XGBoost (Final Model)

After model comparison and tuning, XGBoost showed the best accuracy, precision, and recall.
The final model was saved as xgb_churn_best.pkl for deployment.

Architecture

FastAPI serves as the inference API.

Streamlit provides a web interface for predictions.

Prometheus collects system and prediction metrics.

Grafana visualizes metrics like request latency and churn distribution.

Docker Compose orchestrates all services for easy setup.

API Example

Input:

{
  "MonthlyCharges": 75.0,
  "Tenure": 5,
  "TotalCharges": 500.0,
  "Contract": "Month-to-month",
  "InternetService": "DSL",
  "PaymentMethod": "Electronic check",
  "PaperlessBilling": "Yes",
  "MultipleLines": "Yes",
  "OnlineBackup": "Yes"
}


Output:

{
  "prediction": "Customer is likely to churn",
  "churn_probability": 0.519
}

Monitoring with Prometheus and Grafana

Prometheus collects metrics from FastAPI endpoints like:

Request count

Inference latency

Churn prediction labels (Yes / No)

Grafana Dashboard visualizes:

Request latency over time

Average inference time per request

Gauge chart for live churn probability

Pie chart showing churn vs no-churn ratio

Project Structure
CHURN_PREDICTION_API/
│
├── app/
│   └── main.py
│
├── src/
│   ├── xgb_churn_best.pkl
│   ├── Telecom_processed.csv
│   └── Churn_Prediction.ipynb
│
├── obs/
│   └── prometheus.yml
│
├── assets/
│   ├── FastAPI_docs.png
│   ├── Streamlit_UI.png
│   ├── Prometheus.png
│   └── Grafana_dashboard.png
│
├── Streamlit_app.py
├── docker-compose.yml
├── Dockerfile
├── render.yaml
├── requirements.txt
└── README.md

How to Run Locally

Clone the repository:

git clone https://github.com/Narendra1112/churn-prediction-api.git
cd churn-prediction-api


Install dependencies:

pip install -r requirements.txt


Start the FastAPI server:

uvicorn app.main:app --reload


Launch Streamlit UI:

streamlit run Streamlit_app.py


Start monitoring tools:

docker-compose up -d

Deployment on Render

Use the included render.yaml file for one-click deployment.

services:
  - type: web
    name: churn-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port 10000"
    plan: free

Model Insights

Customers with shorter tenure and higher monthly charges are more likely to churn.

Contracts with month-to-month plans have higher churn rates.

Users with fiber optic internet and electronic check payment show increased churn tendency.

Long-term contracts and automatic payments reduce churn risk.

Future Enhancements

Integrate real customer data pipelines.

Extend metrics for model drift and data quality.

Add automated retraining and deployment workflows using CI/CD.

Host Grafana dashboards online for public demo access.

Live Demo

FastAPI Docs: https://churn-api.onrender.com/docs

API Endpoint: https://churn-api.onrender.com

Streamlit App: Coming Soon