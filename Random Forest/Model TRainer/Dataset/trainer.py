import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

FEATURES_TO_USE = [
    'proto',
    'service',
    'state',
    'spkts',
    'sbytes',
    'dbytes'
]

LABEL_COLUMN = 'label'
print("--- AI NIDS Model Trainer v5.0 (UNSW-NB15) ---")
print("[1] Loading column names from 'NUSW-NB15_features.csv'...")
try:
    col_df = pd.read_csv('NUSW-NB15_features.csv', encoding='ISO-8859-1')
    col_names = col_df['Name'].apply(lambda x: x.strip().lower()).tolist()
except Exception as e:
    print(f"Error loading NUSW-NB15_features.csv: {e}")
    print("Make sure the file is in the same folder.")
    exit()
print("[2] Loading UNSW-NB15 CSVs (this may take a moment)...")
df_list = []
for i in range(1, 5):
    filename = f'UNSW-NB15_{i}.csv'
    try:
        df_part = pd.read_csv(filename, header=None)
        df_list.append(df_part)
    except Exception as e:
        print(f"Warning: Could not load {filename}. Skipping.")
        
if not df_list:
    print("Error: No data files found. Please download UNSW-NB15_1.csv, etc.")
    exit()

df = pd.concat(df_list, ignore_index=True)
df.columns = col_names
print(f"    Loaded {len(df)} total rows.")
print("[3] Processing data...")

df['service'] = df['service'].replace('-', 'other')
df['state'] = df['state'].replace('-', 'other')
dummy_row = {
    'proto': 'other',
    'service': 'other',
    'state': 'other',
    'spkts': 0,
    'sbytes': 0,
    'dbytes': 0,
    'label': 0
}
df = pd.concat([df, pd.DataFrame([dummy_row])], ignore_index=True)
print("    Added dummy row for 'proto' = 'other'.")
encoders = {}
for col in ['proto', 'service', 'state']:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])
    encoders[col] = encoder
    print(f"    Encoded '{col}' column.")
  
print("[4] Separating features and labels...")
X = df[FEATURES_TO_USE]
y = df[LABEL_COLUMN] 

print("[5] Training the AI model (RandomForest)...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X, y)
print("[6] Saving the model and encoders...")

joblib.dump(model, 'nids_model.pkl')
joblib.dump(encoders, 'encoders.pkl')

print("\n--- Training Complete! ---")
print("Two files have been created:")
print("1. nids_model.pkl (The v5 'brain')")
print("2. encoders.pkl (The v5 'dictionary')")
