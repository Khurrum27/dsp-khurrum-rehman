import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import joblib
import os

MODELS_PATH = os.path.join(os.path.dirname(__file__), "..", "models")


def preprocess_data(
    X: pd.DataFrame,
    categorical_features,
    continuous_features,
    encoder=None,
    scaler=None,
    imputer_cat=None,
    imputer_cont=None,
    fit=False,
):
    if fit:
        imputer_cat = SimpleImputer(strategy="most_frequent")
        imputer_cont = SimpleImputer(strategy="mean")
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        scaler = StandardScaler()

        X_cat = imputer_cat.fit_transform(X[categorical_features])
        X_cat_enc = encoder.fit_transform(X_cat)
        X_cont = imputer_cont.fit_transform(X[continuous_features])
        X_cont_scaled = scaler.fit_transform(X_cont)

        joblib.dump(encoder, os.path.join(MODELS_PATH, "encoder.joblib"))
        joblib.dump(scaler, os.path.join(MODELS_PATH, "scaler.joblib"))
        joblib.dump(
            imputer_cat, os.path.join(MODELS_PATH, "imputer_cat.joblib")
        )
        joblib.dump(
            imputer_cont, os.path.join(MODELS_PATH, "imputer_cont.joblib")
        )
    else:
        X_cat = imputer_cat.transform(X[categorical_features])
        X_cat_enc = encoder.transform(X_cat)
        X_cont = imputer_cont.transform(X[continuous_features])
        X_cont_scaled = scaler.transform(X_cont)

    return np.hstack([X_cat_enc, X_cont_scaled])
