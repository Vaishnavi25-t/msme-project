# ============================================================
# generate_dataset.py
# Creates 600 fake (synthetic) MSME business records
# Run this FIRST before train_models.py
# ============================================================
# HOW TO RUN:
#   python generate_dataset.py
# OUTPUT:
#   msme_dataset.csv  (600 rows of simulated data)
# ============================================================

import pandas as pd
import numpy as np
import random

# Fix random seed so you get the same data every time
random.seed(42)
np.random.seed(42)

# ----------------------------------------------------------
# Sector weights for SC-LSS formula
# Different sectors have different financial patterns
# ----------------------------------------------------------
SECTOR_WEIGHTS = {
    'Retail':        {'ER': 0.35, 'RS': 0.15, 'CBS': 0.30, 'BRS': 0.20},
    'Manufacturing': {'ER': 0.25, 'RS': 0.30, 'CBS': 0.25, 'BRS': 0.20},
    'Wholesale':     {'ER': 0.20, 'RS': 0.35, 'CBS': 0.25, 'BRS': 0.20},
    'Food_Beverage': {'ER': 0.35, 'RS': 0.10, 'CBS': 0.25, 'BRS': 0.30},
    'Textile':       {'ER': 0.25, 'RS': 0.30, 'CBS': 0.20, 'BRS': 0.25},
}

# ----------------------------------------------------------
# Sector financial profiles
# Each sector has different typical sales, expenses, etc.
# ----------------------------------------------------------
PROFILES = {
    'Retail': {
        'sales':   (8000, 60000),
        'expense': {'low':(0.45,0.65), 'medium':(0.70,0.88), 'high':(0.90,1.20)},
        'cash':    {'low':(18,35),     'medium':(6,18),       'high':(1,6)},
        'overdue': {'low':(0.00,0.10), 'medium':(0.10,0.30),  'high':(0.30,0.60)},
        'delay':   {'low':(0,10),      'medium':(10,25),       'high':(25,50)},
    },
    'Manufacturing': {
        'sales':   (20000, 120000),
        'expense': {'low':(0.55,0.72), 'medium':(0.72,0.92), 'high':(0.92,1.30)},
        'cash':    {'low':(20,40),     'medium':(8,20),       'high':(2,8)},
        'overdue': {'low':(0.05,0.20), 'medium':(0.20,0.50),  'high':(0.50,0.85)},
        'delay':   {'low':(10,30),     'medium':(30,60),       'high':(60,90)},
    },
    'Wholesale': {
        'sales':   (30000, 200000),
        'expense': {'low':(0.60,0.75), 'medium':(0.75,0.90), 'high':(0.90,1.25)},
        'cash':    {'low':(15,30),     'medium':(5,15),       'high':(1,5)},
        'overdue': {'low':(0.10,0.25), 'medium':(0.25,0.55),  'high':(0.55,0.90)},
        'delay':   {'low':(15,40),     'medium':(40,70),       'high':(70,90)},
    },
    'Food_Beverage': {
        'sales':   (5000, 40000),
        'expense': {'low':(0.50,0.68), 'medium':(0.68,0.90), 'high':(0.90,1.30)},
        'cash':    {'low':(10,25),     'medium':(3,10),       'high':(0.5,3)},
        'overdue': {'low':(0.00,0.05), 'medium':(0.05,0.15),  'high':(0.15,0.40)},
        'delay':   {'low':(0,7),       'medium':(7,20),        'high':(20,45)},
    },
    'Textile': {
        'sales':   (15000, 90000),
        'expense': {'low':(0.52,0.70), 'medium':(0.70,0.90), 'high':(0.90,1.28)},
        'cash':    {'low':(16,32),     'medium':(6,16),       'high':(1,6)},
        'overdue': {'low':(0.08,0.22), 'medium':(0.22,0.50),  'high':(0.50,0.88)},
        'delay':   {'low':(10,35),     'medium':(35,65),       'high':(65,90)},
    },
}


def compute_sc_lss(sector, daily_sales, daily_expenses,
                   cash_balance, total_rec, overdue_rec, monthly_exp):
    """
    Computes the Sector-Calibrated Liquidity Stress Score.
    Returns all 4 components + final score + survival days.
    """
    w = SECTOR_WEIGHTS[sector]

    # Component 1: Expense Ratio
    ER = min((daily_expenses / daily_sales) * 100, 100) if daily_sales > 0 else 100

    # Component 2: Receivables Stress
    RS = (overdue_rec / total_rec * 100) if total_rec > 0 else 0.0

    # Component 3: Cash Buffer Stress
    buffer = (cash_balance / monthly_exp * 100) if monthly_exp > 0 else 100
    CBS = max(0.0, 100 - buffer)

    # Component 4: Burn Rate Stress
    burn = max(0, daily_expenses - daily_sales)
    if burn > 0:
        survival = cash_balance / burn
        BRS = max(0.0, 100 - (survival / 30) * 100)
    else:
        survival = 999
        BRS = 0.0

    sc_lss = round(min(
        w['ER'] * ER + w['RS'] * RS + w['CBS'] * CBS + w['BRS'] * BRS,
        100
    ), 2)

    # Also compute fixed-weight version for comparison
    fixed = round(min(0.30*ER + 0.25*RS + 0.25*CBS + 0.20*BRS, 100), 2)

    return round(ER,2), round(RS,2), round(CBS,2), round(BRS,2), sc_lss, fixed, round(min(survival,999),1)


# ----------------------------------------------------------
# Generate 600 records (120 per sector, 40 per stress level)
# ----------------------------------------------------------
records = []
levels  = ['low', 'medium', 'high']

for sector, profile in PROFILES.items():
    for i in range(120):
        level = levels[i % 3]

        sales = random.uniform(*profile['sales'])
        ef_lo, ef_hi = profile['expense'][level]
        expenses = sales * random.uniform(ef_lo, ef_hi)
        cm_lo, cm_hi = profile['cash'][level]
        cash = sales * random.uniform(cm_lo, cm_hi)
        or_lo, or_hi = profile['overdue'][level]
        overdue_ratio = random.uniform(or_lo, or_hi)
        delay = random.randint(*profile['delay'][level])

        total_rec  = sales * random.uniform(8, 25)
        overdue_rec = total_rec * overdue_ratio
        monthly_exp = expenses * 30

        ER, RS, CBS, BRS, sc_lss, fixed_lss, survival = compute_sc_lss(
            sector, sales, expenses, cash, total_rec, overdue_rec, monthly_exp
        )

        risk = 'Low' if sc_lss <= 30 else ('Medium' if sc_lss <= 60 else 'High')

        records.append({
            'sector':             sector,
            'daily_sales':        round(sales, 2),
            'daily_expenses':     round(expenses, 2),
            'cash_balance':       round(cash, 2),
            'total_receivables':  round(total_rec, 2),
            'overdue_receivables':round(overdue_rec, 2),
            'avg_delay_days':     delay,
            'monthly_expenses':   round(monthly_exp, 2),
            'expense_ratio':      ER,
            'receivables_stress': RS,
            'cash_buffer_stress': CBS,
            'burn_rate_stress':   BRS,
            'survival_days':      survival,
            'fixed_lss':          fixed_lss,
            'sc_lss':             sc_lss,
            'risk_label':         risk,
        })

df = pd.DataFrame(records)
df.to_csv('msme_dataset.csv', index=False)

print("Done! msme_dataset.csv created.")
print(f"Total records : {len(df)}")
print(f"\nRisk distribution:\n{df['risk_label'].value_counts()}")
print(f"\nSector distribution:\n{df['sector'].value_counts()}")