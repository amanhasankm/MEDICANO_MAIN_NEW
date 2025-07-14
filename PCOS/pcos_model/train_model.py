import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib
import os

# Load the dataset
data_path = os.path.join(os.path.dirname(__file__), 'pcos_dataset.csv')
data = pd.read_csv(data_path, sep=',')

print("📄 Raw data preview:")
print(data.head())
print("📄 Columns before cleaning:", data.columns.tolist())

# Clean column names (handle extra spaces)
data.columns = data.columns.str.strip().str.replace(r'\s+', ' ', regex=True)

# Drop any unnecessary columns (e.g., if there's no patient ID or other irrelevant data)
cols_to_drop = []  # Add column names here if needed
data.drop(columns=[col for col in cols_to_drop if col in data.columns], inplace=True)

print("📄 Cleaned columns:", data.columns.tolist())

# Selected features for training (update to match your dataset)
selected_features = [
    'Age', 
    'BMI', 
    'Menstrual_Irregularity', 
    'Testosterone_Level(ng/dL)', 
    'Antral_Follicle_Count'
]

# Validate selected features exist in dataset
missing = [feat for feat in selected_features if feat not in data.columns]
if missing:
    raise ValueError(f"❌ Missing columns in dataset: {missing}")

# Check for target column
target_col = 'PCOS_Diagnosis'  # Assuming 'PCOS_Diagnosis' is the target
if target_col not in data.columns:
    raise ValueError(f"❌ Target column '{target_col}' is missing from dataset.")

# Convert selected feature columns to numeric and fill missing values
for col in selected_features:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Handle missing values by filling with the median of each column (could also drop rows with missing values)
data[selected_features] = data[selected_features].fillna(data[selected_features].median())

# Prepare data for training
X = data[selected_features]
y = data[target_col]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train the model using Random Forest
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model's accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"📊 Model Accuracy on test set: {accuracy:.2f}")

# Save the trained model and scaler
model_dir = os.path.join(os.path.dirname(__file__), 'pcos_model')
os.makedirs(model_dir, exist_ok=True)
joblib.dump(model, os.path.join(model_dir, 'pcos_model.pkl'))
joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))

print("✅ Model and scaler saved successfully.")
print("✅ Trained on features:", selected_features)
