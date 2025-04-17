import pandas as pd
import numpy as np
import joblib
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from house_prices.preprocess import preprocess_data

MODELS_PATH = os.path.join(os.path.dirname(__file__), "..", "models")


def build_model(data: pd.DataFrame) -> dict[str, float]:
    target = "SalePrice"
    categorical_features = ["MSZoning", "Street"]
    continuous_features = ["LotArea", "GrLivArea"]

    X = data[categorical_features + continuous_features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train_processed = preprocess_data(
        X_train, categorical_features, continuous_features, fit=True
    )

    y_train = y_train.fillna(y_train.mean())

    model = LinearRegression()
    model.fit(X_train_processed, y_train)
    joblib.dump(model, os.path.join(MODELS_PATH, "model.joblib"))

    X_test_processed = preprocess_data(
        X_test,
        categorical_features,
        continuous_features,
        encoder=joblib.load(os.path.join(MODELS_PATH, "encoder.joblib")),
        scaler=joblib.load(os.path.join(MODELS_PATH, "scaler.joblib")),
        imputer_cat=joblib.load(
            os.path.join(MODELS_PATH, "imputer_cat.joblib")
        ),
        imputer_cont=joblib.load(
            os.path.join(MODELS_PATH, "imputer_cont.joblib")
        ),
        fit=False,
    )

    y_test = y_test.fillna(y_test.mean())
    y_pred = model.predict(X_test_processed)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    return {"rmse": round(rmse, 2)}
