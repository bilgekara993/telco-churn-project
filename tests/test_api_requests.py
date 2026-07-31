import requests


API_URL = "http://127.0.0.1:8000/predict"


high_risk_customer = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 1,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 95.10,
    "TotalCharges": 95.10
}


low_risk_customer = {
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "Yes",
    "tenure": 60,
    "PhoneService": "Yes",
    "MultipleLines": "Yes",
    "InternetService": "DSL",
    "OnlineSecurity": "Yes",
    "OnlineBackup": "Yes",
    "DeviceProtection": "Yes",
    "TechSupport": "Yes",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Two year",
    "PaperlessBilling": "No",
    "PaymentMethod": (
        "Bank transfer (automatic)"
    ),
    "MonthlyCharges": 65.00,
    "TotalCharges": 3900.00
}


test_customers = {
    "Yüksek riskli müşteri": high_risk_customer,
    "Düşük riskli müşteri": low_risk_customer
}


for customer_name, customer_data in test_customers.items():
    response = requests.post(
        API_URL,
        json=customer_data,
        timeout=10
    )

    print(f"\n{customer_name}")
    print(f"HTTP durum kodu: {response.status_code}")
    print(f"API cevabı: {response.json()}")