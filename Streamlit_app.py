import streamlit as st
import requests
import os

st.set_page_config(page_title="Churn Prediction", layout="centered")
st.title("Customer Churn Prediction")
st.write("Enter customer details to predict churn probability using the trained model.")

# FastAPI endpoint (Render backend)
API_URL = os.environ.get("API_URL", "https://churn-prediction-api-gdae.onrender.com/predict")

# --- Inputs ---
col1, col2 = st.columns(2)
monthly_charges = col1.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=75.0)
total_charges = col2.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, value=500.0)

tenure = st.slider("Tenure (months)", 0, 72, 12)

contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Credit card (automatic)"])

col3, col4, col5 = st.columns(3)
paperless = col3.selectbox("Paperless Billing", ["Yes", "No"])
multi_lines = col4.selectbox("Multiple Lines", ["Yes", "No"])
backup = col5.selectbox("Online Backup", ["Yes", "No"])


if st.button("🔮 Predict Churn"):
    data = {
        "MonthlyCharges": monthly_charges,
        "Tenure": tenure,
        "TotalCharges": total_charges,
        "Contract": contract,
        "InternetService": internet_service,
        "PaymentMethod": payment_method,
        "PaperlessBilling": paperless,
        "MultipleLines": multi_lines,
        "OnlineBackup": backup
    }

    try:
        response = requests.post(API_URL, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()

        st.success(result["prediction"])
        st.metric(label="Churn Probability", value=f"{result['churn_probability'] * 100:.2f}%")

    except requests.exceptions.RequestException as e:
        st.error(f" Could not connect to the prediction API.\n\nDetails: {e}")
