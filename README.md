# Customer Churn Prediction with Real-Time Monitoring


##  Live Demo

**Deployed Application:** [Try it here on Render](https://churn-prediction-api-xk5q.onrender.com/)  
This live web app demonstrates real-time churn prediction powered by **FastAPI** and **Streamlit**.  
Users can input customer details, view churn probabilities instantly, and observe backend metrics integrated via Prometheus and Grafana.

![Streamlit App Demo](https://github.com/Narendra1112/churn-prediction-api/blob/main/assets/Streamlit_UI.png)





## Overview

An end-to-end **Machine Learning** project that predicts telecom customer churn using FastAPI, XGBoost, and Streamlit, with real-time monitoring powered by Prometheus and Grafana.

Churn prediction identifies customers who are likely to stop using a company’s service which is a key challenge in industries like telecom, streaming platforms (e.g., Netflix), or subscription businesses (e.g., Amazon Prime). By predicting who might leave, companies can proactively offer personalized discounts, improved support, or loyalty rewards to retain them.

This project demonstrates a production-ready MLOps workflow, including model serving, containerized deployment, and live performance tracking, bridging the gap between machine learning models and real-world business impact.

## Tech Stack

Backend: FastAPI, Python, XGBoost, Pandas
Frontend: Streamlit
Monitoring: Prometheus, Grafana
Containerization: Docker & Docker-Compose

## Architecture

FastAPI → model inference endpoint

Streamlit → user-friendly interface

Prometheus → collects API metrics

Grafana → visualizes churn data and system latency

# Dataset

The dataset used in this project comes from the [Kaggle](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset)
, which is also available on [IBM sample data](https://www.ibm.com/docs/en/cognos-analytics/11.1.0?).
It contains information about telecom customers, including:

Demographics: gender, age, marital status, and dependents

Account Details: contract type, billing method, payment type, monthly charges, and total charges

Service Usage: phone services, internet type, online security, backup, device protection, tech support, and streaming services

Churn Indicator: whether the customer discontinued the service in the previous month

## How it was used

The dataset was cleaned and preprocessed to handle missing values and encode categorical variables. Feature importance was analyzed using XGBoost, and the top 10 predictors (such as tenure, monthly charges, and contract type) were selected for model training. The final model was deployed via FastAPI for real-time churn prediction and visualized through Streamlit and Grafana dashboards.

## Features

Real-time churn prediction API (FastAPI)

Streamlit dashboard for live user input

Prometheus metrics for http_requests_total

Grafana dashboards Pie churn stats, Total Number of requests, Prometheus scrape duration

Docker-based setup for full reproducibility

##  Run Locally

git clone https://github.com/Narendra1112/churn-prediction-api.git
cd churn-prediction-api
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run Streamlit_app.py
docker-compose up -d


# API Example

## Input

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


## Output

{
  "prediction": "Customer is likely to churn",
  "churn_probability": 0.519
}

## Monitoring Views

FastAPI Docs: http://localhost:8000/docs
![image](https://github.com/Narendra1112/churn-prediction-api/blob/main/assets/Fastapi_docs.png)

Streamlit UI: http://localhost:8501
![image](https://github.com/Narendra1112/churn-prediction-api/blob/main/assets/Streamlit_UI.png)

Prometheus: http://localhost:9090
![image](https://github.com/Narendra1112/churn-prediction-api/blob/main/assets/Prometheus.png)

Grafana: http://localhost:3000
![image](https://github.com/Narendra1112/churn-prediction-api/blob/main/assets/Grafana_dashboard.png)


## Key Insights

Short-tenure customers are more likely to churn.

Month-to-month contracts and higher charges correlate with churn.

Auto-payment and long-term contracts reduce churn rates.

# License

This project is licensed under the MIT License — you’re free to use, modify, and distribute it with proper attribution.


