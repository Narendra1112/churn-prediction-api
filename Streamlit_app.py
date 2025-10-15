import streamlit as st
import requests

st.set_page_config(page_title="Churn Prediction", layout="centered")
st.title("Customer Churn Prediction")
st.write("Enter details below to predict churn probability")

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

# --- Predict Button ---
if st.button(" Predict Churn"):
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

    response = requests.post("http://127.0.0.1:8000/predict", json=data)

    if response.status_code == 200:
        result = response.json()
        st.subheader(f"Prediction: {result['prediction']}")
        st.subheader(f"Churn Probability: {result['churn_probability'] * 100:.2f}%")
    else:
        st.error("Error: Could not get prediction. Check if FastAPI is running.")
