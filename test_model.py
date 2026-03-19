import joblib
import pandas as pd

# Load saved model
model = joblib.load("model.pkl")
print("✅ Model loaded successfully!")

# Quick test
df = pd.read_csv("data/dataset.csv")
df = df.drop(columns=['Index'])
X = df.drop(columns=['class'])

sample = X.iloc[0:1]  # take first row
result = model.predict(sample)

print("Prediction:", "Phishing 🚨" if result[0] == -1 else "Legitimate ✅")