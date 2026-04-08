# ============================================================
# train_models.py
# Trains 2 ML models and saves them as .pkl files
# Run this AFTER generate_dataset.py
# ============================================================
# HOW TO RUN:
#   python train_models.py
# OUTPUT:
#   regressor.pkl       (predicts LSS score number)
#   classifier.pkl      (predicts Low/Medium/High risk)
#   label_encoder.pkl   (helper file for classifier)
#   model_config.json   (sector weights, feature names)
# ============================================================

import pandas as pd
import numpy as np
import pickle
import json

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.linear_model    import LinearRegression
from sklearn.tree            import DecisionTreeClassifier
from sklearn.preprocessing   import LabelEncoder, OneHotEncoder
from sklearn.compose         import ColumnTransformer
from sklearn.pipeline        import Pipeline
from sklearn.metrics         import (mean_absolute_error, mean_squared_error,
                                     r2_score, accuracy_score, classification_report)

# ----------------------------------------------------------
# Load dataset
# ----------------------------------------------------------
df = pd.read_csv('msme_dataset.csv')
print(f"Loaded {len(df)} records.\n")

# Features the model will learn from
CATEGORICAL = ['sector']
NUMERIC     = ['daily_sales','daily_expenses','cash_balance',
               'total_receivables','overdue_receivables',
               'avg_delay_days','monthly_expenses']
ALL_FEATURES = CATEGORICAL + NUMERIC

X       = df[ALL_FEATURES]
y_score = df['sc_lss']       # what regression model predicts
y_risk  = df['risk_label']   # what classifier predicts

# ----------------------------------------------------------
# Preprocessor: converts sector text to numbers (one-hot)
# ----------------------------------------------------------
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL),
    ('num', 'passthrough', NUMERIC),
])

# Split: 80% training, 20% testing
X_train, X_test, ys_train, ys_test, yr_train, yr_test = train_test_split(
    X, y_score, y_risk, test_size=0.2, random_state=42, stratify=y_risk
)

# ----------------------------------------------------------
# MODEL 1: Linear Regression (predicts the score 0-100)
# ----------------------------------------------------------
print("=" * 50)
print("MODEL 1: Linear Regression (SC-LSS score)")
print("=" * 50)

lr = Pipeline([('pre', preprocessor), ('model', LinearRegression())])
lr.fit(X_train, ys_train)
pred_score = lr.predict(X_test)

print(f"MAE  : {mean_absolute_error(ys_test, pred_score):.2f}")
print(f"RMSE : {np.sqrt(mean_squared_error(ys_test, pred_score)):.2f}")
print(f"R²   : {r2_score(ys_test, pred_score):.4f}")
print()

# ----------------------------------------------------------
# MODEL 2: Decision Tree (predicts Low / Medium / High)
# ----------------------------------------------------------
print("=" * 50)
print("MODEL 2: Decision Tree (Risk Label)")
print("=" * 50)

le = LabelEncoder()
yr_train_enc = le.fit_transform(yr_train)
yr_test_enc  = le.transform(yr_test)

dt = Pipeline([
    ('pre', preprocessor),
    ('model', DecisionTreeClassifier(max_depth=7, min_samples_split=8, random_state=42))
])
dt.fit(X_train, yr_train_enc)
pred_risk = dt.predict(X_test)

print(f"Test Accuracy : {accuracy_score(yr_test_enc, pred_risk)*100:.2f}%")
print()
print(classification_report(yr_test_enc, pred_risk, target_names=le.classes_))

cv = cross_val_score(dt, X, le.transform(y_risk),
                     cv=StratifiedKFold(5, shuffle=True, random_state=42))
print(f"5-Fold CV Accuracy: {cv.mean()*100:.2f}% ± {cv.std()*100:.2f}%")

# ----------------------------------------------------------
# Save everything to disk
# ----------------------------------------------------------
with open('regressor.pkl',     'wb') as f: pickle.dump(lr, f)
with open('classifier.pkl',    'wb') as f: pickle.dump(dt, f)
with open('label_encoder.pkl', 'wb') as f: pickle.dump(le, f)

config = {
    'categorical_features': CATEGORICAL,
    'numeric_features':     NUMERIC,
    'sector_weights': {
        'Retail':        {'ER': 0.35, 'RS': 0.15, 'CBS': 0.30, 'BRS': 0.20},
        'Manufacturing': {'ER': 0.25, 'RS': 0.30, 'CBS': 0.25, 'BRS': 0.20},
        'Wholesale':     {'ER': 0.20, 'RS': 0.35, 'CBS': 0.25, 'BRS': 0.20},
        'Food_Beverage': {'ER': 0.35, 'RS': 0.10, 'CBS': 0.25, 'BRS': 0.30},
        'Textile':       {'ER': 0.25, 'RS': 0.30, 'CBS': 0.20, 'BRS': 0.25},
    }
}
with open('model_config.json', 'w') as f: json.dump(config, f, indent=2)

print("\nAll files saved:")
print("  regressor.pkl, classifier.pkl, label_encoder.pkl, model_config.json")