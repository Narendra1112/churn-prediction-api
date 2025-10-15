from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

# ----------------------------------------------------
# 🚀 App Initialization
# ----------------------------------------------------
app = FastAPI(
    title="Customer Churn Prediction API (Top 10 Features)",
    description="Predict customer churn using top 10 most important features and XGBoost.",
    version="2.0.0"
)

# ----------------------------------------------------
# 🧩 Prometheus Instrumentation
# ----------------------------------------------------
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app)

# ✅ Custom Prometheus Counter (for Pie Chart)
PREDICTED_LABELS = Counter(
    "predicted_labels_total",
    "Count of churn predictions by label",
    ["label"]
)

# ----------------------------------------------------
# 🧠 Model + Columns
# ----------------------------------------------------
model = joblib.load("src/xgb_churn_best.pkl")

model_columns = [
    'Gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Tenure',
    'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
    'PaperlessBilling', 'MonthlyCharges', 'TotalCharges',
    'InternetService_Fiber_optic', 'InternetService_No',
    'Contract_One_year', 'Contract_Two_year',
    'PaymentMethod_Credit_card_automatic',
    'PaymentMethod_Electronic_check', 'PaymentMethod_Mailed_check'
]

# ----------------------------------------------------
# 🧾 Input Schema (Top 10 Features)
# ----------------------------------------------------
class CustomerInput(BaseModel):
    MonthlyCharges: float
    Tenure: float
    TotalCharges: float
    Contract: str                  # "Month-to-month", "One year", "Two year"
    InternetService: str           # "DSL", "Fiber optic", "No"
    PaymentMethod: str             # "Electronic check", "Mailed check", "Credit card (automatic)"
    PaperlessBilling: str          # "Yes" / "No"
    MultipleLines: str             # "Yes" / "No"
    OnlineBackup: str              # "Yes" / "No"

# ----------------------------------------------------
# 🧮 Encoding Function
# ----------------------------------------------------
def encode_input(user_data: dict):
    df = pd.DataFrame([user_data])

    # Contract encoding
    df['Contract_One_year'] = (df['Contract'] == 'One year').astype(int)
    df['Contract_Two_year'] = (df['Contract'] == 'Two year').astype(int)
    df.drop('Contract', axis=1, inplace=True)

    # InternetService encoding
    df['InternetService_Fiber_optic'] = (df['InternetService'] == 'Fiber optic').astype(int)
    df['InternetService_No'] = (df['InternetService'] == 'No').astype(int)
    df.drop('InternetService', axis=1, inplace=True)

    # PaymentMethod encoding
    df['PaymentMethod_Electronic_check'] = (df['PaymentMethod'] == 'Electronic check').astype(int)
    df['PaymentMethod_Mailed_check'] = (df['PaymentMethod'] == 'Mailed check').astype(int)
    df['PaymentMethod_Credit_card_automatic'] = (df['PaymentMethod'] == 'Credit card (automatic)').astype(int)
    df.drop('PaymentMethod', axis=1, inplace=True)

    # Binary yes/no
    df['PaperlessBilling'] = df['PaperlessBilling'].map({'Yes': 1, 'No': 0})
    df['MultipleLines'] = df['MultipleLines'].map({'Yes': 1, 'No': 0})
    df['OnlineBackup'] = df['OnlineBackup'].map({'Yes': 1, 'No': 0})

    # Fill remaining columns
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[model_columns]
    return df

# ----------------------------------------------------
# 🔮 Prediction Endpoint
# ----------------------------------------------------
@app.post("/predict")
def predict_churn(data: CustomerInput):
    df = encode_input(data.dict())
    prob = model.predict_proba(df)[0][1]
    prediction = "Yes" if prob >= 0.5 else "No"

    # ✅ Record prediction in Prometheus counter
    PREDICTED_LABELS.labels(label=prediction).inc()

    return {
        "prediction": (
            "Customer is likely to churn" if prediction == "Yes"
            else "Customer is not likely to churn"
        ),
        "churn_probability": round(float(prob), 3)
    }

# ----------------------------------------------------
# 💚 Health Check
# ----------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "OK", "message": "Churn API is running Good"}
