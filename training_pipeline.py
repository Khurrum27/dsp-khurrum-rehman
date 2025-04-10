import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_log_error

def load_data(train_path: str, test_path: str):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df

def preprocess_data(train_df: pd.DataFrame, test_df: pd.DataFrame):
    num_features = ["GrLivArea", "LotArea"]
    cat_features = ["Neighborhood", "HouseStyle"]
    target = "SalePrice"

    selected_features = num_features + cat_features + [target]
    train_selected = train_df[selected_features].copy()
    test_selected = test_df[num_features + cat_features].copy()

    # Handle missing values
    for col in num_features:
        train_selected[col] = train_selected[col].fillna(train_selected[col].median())
        test_selected[col] = test_selected[col].fillna(test_selected[col].median())

    for col in cat_features:
        train_selected[col] = train_selected[col].fillna("Unknown")
        test_selected[col] = test_selected[col].fillna("Unknown")

    # ✅ Consistent one-hot encoding by fitting on combined data
    combined_cat = pd.concat([train_selected[cat_features], test_selected[cat_features]], axis=0)
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoder.fit(combined_cat)

    encoded_train = pd.DataFrame(encoder.transform(train_selected[cat_features]))
    encoded_test = pd.DataFrame(encoder.transform(test_selected[cat_features]))

    encoded_train.columns = encoder.get_feature_names_out(cat_features)
    encoded_test.columns = encoder.get_feature_names_out(cat_features)

    encoded_train.reset_index(drop=True, inplace=True)
    encoded_test.reset_index(drop=True, inplace=True)

    train_selected = train_selected.drop(columns=cat_features).reset_index(drop=True)
    test_selected = test_selected.drop(columns=cat_features).reset_index(drop=True)

    train_final = pd.concat([train_selected, encoded_train], axis=1)
    test_final = pd.concat([test_selected, encoded_test], axis=1)

    # Scaling
    scaler = StandardScaler()
    train_final[num_features] = scaler.fit_transform(train_final[num_features])
    test_final[num_features] = scaler.transform(test_final[num_features])

    return train_final, test_final, encoder, scaler

def train_model(train_final: pd.DataFrame):
    X_train = train_final.drop(columns=["SalePrice"])
    y_train = train_final["SalePrice"]

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_train, y_train

def compute_rmsle(y_true: np.ndarray, y_pred: np.ndarray, precision: int = 2) -> float:
    rmsle = np.sqrt(mean_squared_log_error(y_true, y_pred))
    return round(rmsle, precision)

def run_pipeline(train_path: str, test_path: str):
    train_df, test_df = load_data(train_path, test_path)
    train_final, test_final, encoder, scaler = preprocess_data(train_df, test_df)
    model, X_train, y_train = train_model(train_final)

    preds = model.predict(X_train)
    score = compute_rmsle(y_train, preds)

    print(f"✅ RMSLE Score: {score}")
    
    return train_final  # <- Needed for reproducibility test

if __name__ == "__main__":
    train_path = r"E:\Python tasks\dsp-khurrum-rehman\PW2\data\train.csv"
    test_path = r"E:\Python tasks\dsp-khurrum-rehman\PW2\data\test.csv"
    run_pipeline(train_path, test_path)
