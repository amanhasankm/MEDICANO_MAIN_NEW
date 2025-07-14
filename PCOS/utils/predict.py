import joblib
import numpy as np
import os

# Load model and scaler (ensure paths are correct)
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pcos_model', 'pcos_model.pkl'))
scaler_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pcos_model', 'scaler.pkl'))

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

def predict_pcos(features: np.ndarray) -> int:
    """
    Predict whether the patient has PCOS based on input features.
    Input: features - a NumPy array of shape (1, 3)
    Output: prediction - 0 or 1
    """
    # Scale features
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)
    return int(prediction[0])
