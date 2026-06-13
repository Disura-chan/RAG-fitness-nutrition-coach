import joblib
import pandas as pd

model = joblib.load("models/obesity_model.pkl")
encoders = joblib.load("models/obesity_encoders.pkl")

def predict_obesity(user_data):

    df = pd.DataFrame([user_data])

    for col in encoders:

        if col == "NObeyesdad":
            continue

        df[col] = encoders[col].transform(
            df[col]
        )

    prediction = model.predict(df)

    risk = encoders[
        "NObeyesdad"
    ].inverse_transform(
        prediction
    )

    return risk[0]