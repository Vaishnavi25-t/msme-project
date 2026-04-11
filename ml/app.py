# ============================================================
# app.py  —  Python ML Prediction Server
# Receives data from Java backend, returns SC-LSS result
# ============================================================
# HOW TO RUN (AFTER running train_models.py):
#   python app.py
# SERVER RUNS ON:
#   http://localhost:5000
# ============================================================

from flask       import Flask, request, jsonify
from flask_cors  import CORS
import pickle, json, pandas as pd

app = Flask(__name__)
CORS(app)   # Allow Java to call this server

# ----------------------------------------------------------
# Load the trained models (must run train_models.py first)
# ----------------------------------------------------------
with open('regressor.pkl',     'rb') as f: regressor    = pickle.load(f)
with open('classifier.pkl',    'rb') as f: classifier   = pickle.load(f)
with open('label_encoder.pkl', 'rb') as f: label_encoder = pickle.load(f)
with open('model_config.json', 'r')  as f: config        = json.load(f)

SECTOR_WEIGHTS   = config['sector_weights']
NUMERIC_FEATURES = config['numeric_features']


# ----------------------------------------------------------
# SC-LSS formula  (same formula as generate_dataset.py)
# ----------------------------------------------------------
def compute_sc_lss(data):
    sector       = data['sector']
    daily_sales  = float(data['daily_sales'])
    daily_exp    = float(data['daily_expenses'])
    cash         = float(data['cash_balance'])
    total_rec    = float(data['total_receivables'])
    overdue_rec  = float(data['overdue_receivables'])
    monthly_exp  = float(data['monthly_expenses'])

    if sector not in SECTOR_WEIGHTS:
        raise ValueError(f"Unknown sector '{sector}'. Supported: {list(SECTOR_WEIGHTS.keys())}")

    w = SECTOR_WEIGHTS[sector]

    ER  = min((daily_exp / daily_sales) * 100, 100) if daily_sales > 0 else 100
    RS  = (overdue_rec / total_rec * 100) if total_rec > 0 else 0.0
    CBS = max(0.0, 100 - (cash / monthly_exp * 100)) if monthly_exp > 0 else 0.0

    burn = max(0, daily_exp - daily_sales)
    if burn > 0:
        survival = int(cash / burn)
        BRS = max(0.0, 100 - (survival / 30) * 100)
    else:
        survival = 999
        BRS = 0.0

    sc_lss    = round(min(w['ER']*ER + w['RS']*RS + w['CBS']*CBS + w['BRS']*BRS, 100), 2)
    fixed_lss = round(min(0.30*ER   + 0.25*RS  + 0.25*CBS  + 0.20*BRS,          100), 2)

    return {
        'expense_ratio':      round(ER, 2),
        'receivables_stress': round(RS, 2),
        'cash_buffer_stress': round(CBS, 2),
        'burn_rate_stress':   round(BRS, 2),
        'sc_lss_score':       sc_lss,
        'fixed_lss_score':    fixed_lss,
        'lss_difference':     round(sc_lss - fixed_lss, 2),
        'survival_days':      survival,
        'weights_used':       w,
    }


# ----------------------------------------------------------
# /api/predict  —  main endpoint called by Java backend
# ----------------------------------------------------------
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Check all required fields are present
        required = ['sector','daily_sales','daily_expenses','cash_balance',
                    'total_receivables','overdue_receivables',
                    'avg_delay_days','monthly_expenses']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Compute SC-LSS using formula
        result = compute_sc_lss(data)

        # Also use ML classifier to predict risk label
        features = pd.DataFrame([{
            'sector':              data['sector'],
            'daily_sales':         float(data['daily_sales']),
            'daily_expenses':      float(data['daily_expenses']),
            'cash_balance':        float(data['cash_balance']),
            'total_receivables':   float(data['total_receivables']),
            'overdue_receivables': float(data['overdue_receivables']),
            'avg_delay_days':      float(data['avg_delay_days']),
            'monthly_expenses':    float(data['monthly_expenses']),
        }])

        encoded_label = classifier.predict(features)[0]
        risk_label    = label_encoder.inverse_transform([encoded_label])[0]

        # Build alert message
        score = result['sc_lss_score']
        if score <= 30:
            alert = "Business is financially stable. Keep monitoring regularly."
        elif score <= 60:
            alert = "Warning: Cash flow stress detected. Review expenses and collect overdue payments."
        else:
            days = result['survival_days']
            if days < 999:
                alert = f"Critical: Cash crisis likely in {days} days. Immediate action needed!"
            else:
                alert = "Critical: High stress detected. Review all financial indicators immediately."

        return jsonify({
            **result,
            'risk_label':    risk_label,
            'alert_message': alert,
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


# ----------------------------------------------------------
# /api/health  —  test if server is running
# ----------------------------------------------------------
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'Python ML server is running'})


# ----------------------------------------------------------
# /api/sectors  —  returns supported sectors and weights
# ----------------------------------------------------------
@app.route('/api/sectors', methods=['GET'])
def sectors():
    return jsonify({
        'sectors': list(SECTOR_WEIGHTS.keys()),
        'weights': SECTOR_WEIGHTS,
    })


if __name__ == '__main__':
    print("Starting Python ML server on http://localhost:5000")
    app.run(debug=True, port=5000)