import pandas as pd
import joblib
import os
from house_prices.preprocess import preprocess_data

MODELS_PATH = os.path.join(os.path.dirname(__file__), "..", "models")


def make_predictions(input_data: pd.DataFrame) -> pd.DataFrame:
    model = joblib.load(os.path.join(MODELS_PATH, "model.joblib"))
    encoder = joblib.load(os.path.join(MODELS_PATH, "encoder.joblib"))
    scaler = joblib.load(os.path.join(MODELS_PATH, "scaler.joblib"))
    imputer_cat = joblib.load(os.path.join(MODELS_PATH, "imputer_cat.joblib"))
    imputer_cont = joblib.load(
        os.path.join(MODELS_PATH, "imputer_cont.joblib")
    )

    categorical_features = ["MSZoning", "Street"]
    continuous_features = ["LotArea", "GrLivArea"]

    X_processed = preprocess_data(
        input_data[categorical_features + continuous_features],
        categorical_features,
        continuous_features,
        encoder=encoder,
        scaler=scaler,
        imputer_cat=imputer_cat,
        imputer_cont=imputer_cont,
        fit=False,
    )

    predictions = model.predict(X_processed)
    return pd.DataFrame({"Predicted_SalePrice": predictions})
