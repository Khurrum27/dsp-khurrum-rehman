import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_log_error

# Load data
train = pd.read_csv("../data/train.csv")
test = pd.read_csv("../data/test.csv")

# Display first few rows of training data
train.head()

# Select Features
continuous_features = ["LotArea", "GrLivArea"]
categorical_features = ["MSZoning", "Street"]

target = "SalePrice"
X = train[continuous_features + categorical_features]
y = train[target]

# Handle missing values
X.fillna(X.median(), inplace=True)  # For continuous features
X.fillna("Missing", inplace=True)   # For categorical features

# Encoding categorical features
encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
X_encoded = encoder.fit_transform(X[categorical_features])
X_encoded = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out(categorical_features))

# Scaling continuous features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X[continuous_features])
X_scaled = pd.DataFrame(X_scaled, columns=continuous_features)

# Combine processed features
X_final = pd.concat([X_scaled, X_encoded], axis=1)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

def compute_rmsle(y_test: np.ndarray, y_pred: np.ndarray, precision: int = 2) -> float:
    rmsle = np.sqrt(mean_squared_log_error(y_test, y_pred))
    return round(rmsle, precision)

# Evaluate model
rmsle_score = compute_rmsle(y_test, y_pred)
print(f'RMSLE Score: {rmsle_score}')
