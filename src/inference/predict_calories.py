import joblib
import pandas as pd

model = joblib.load(
    "models/calories_model.pkl"
)

encoder = joblib.load(
    "models/calories_gender_encoder.pkl"
)

def predict_calories(data):

    df = pd.DataFrame([data])

    df["Gender"] = encoder.transform(
        df["Gender"]
    )

    prediction = model.predict(df)

    return round(
        prediction[0],
        2
    )