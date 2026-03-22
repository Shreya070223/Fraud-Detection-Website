import pandas as pd

# Load dataset
df = pd.read_csv("data/dataset.csv")

# See first 5 rows
print(df.head())

# See shape (rows, columns)
print("Shape:", df.shape)

# See column names
print("Columns:", df.columns.tolist())

# ✅ Fix here — your dataset uses 'class' not 'Result'
print(df['class'].value_counts())