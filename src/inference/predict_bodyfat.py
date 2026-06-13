import joblib
import pandas as pd

model = joblib.load(
    "models/body_fat_model.pkl"
)

def predict_bodyfat(data):

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    return round(
        prediction[0],
        2
    )