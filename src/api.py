from pathlib import Path
import json

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "final_churn_pipeline.joblib"
)

CONFIG_PATH = (
    PROJECT_ROOT
    / "models"
    / "threshold_config.json"
)


final_pipeline = joblib.load(MODEL_PATH)

with open(
    CONFIG_PATH,
    "r",
    encoding="utf-8"
) as file:
    threshold_config = json.load(file)


OPTIMAL_THRESHOLD = threshold_config.get("decision_threshold")

if OPTIMAL_THRESHOLD is None:
    raise ValueError(
        "Config dosyasında 'decision_threshold' bulunamadı."
    )


app = FastAPI(
    title="Telco Customer Churn API",
    description=(
        "Müşteri bilgilerini kullanarak churn "
        "olasılığı tahmin eden servis."
    ),
    version="1.0.0"
)


class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int = Field(ge=0, le=1)
    Partner: str
    Dependents: str
    tenure: int = Field(ge=0)
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)


@app.get("/")
def home():
    return {
        "message": "Telco Churn API çalışıyor.",
        "docs": "/docs"
    }



@app.post("/predict")
def predict_churn(customer: CustomerData):
    try:
        customer_dict = customer.model_dump()

        customer_df = pd.DataFrame(
            [customer_dict]
        )

        churn_probability = (
            final_pipeline.predict_proba(
                customer_df
            )[0, 1]
        )

        churn_prediction = int(
            churn_probability
            >= OPTIMAL_THRESHOLD
        )

        return {
            "churn_probability": round(
                float(churn_probability),
                4
            ),
            "churn_prediction": churn_prediction,
            "churn_label": (
                "Yes"
                if churn_prediction == 1
                else "No"
            ),
            "threshold": round(
                float(OPTIMAL_THRESHOLD),
                4
            )
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Tahmin sırasında hata oluştu: {error}"
        ) from error