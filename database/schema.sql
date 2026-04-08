-- ============================================================
-- MSME Working Capital Stress Analyzer
-- Run this ENTIRE file in MySQL Workbench once
-- ============================================================

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS msme_analyzer;

-- Step 2: Tell MySQL to use it
USE msme_analyzer;

-- Step 3: Table for businesses
CREATE TABLE IF NOT EXISTS businesses (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    business_name VARCHAR(100) NOT NULL,
    owner_name    VARCHAR(100),
    sector        VARCHAR(50),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 4: Table for daily sales and expense entries
CREATE TABLE IF NOT EXISTS daily_transactions (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    business_id    INT NOT NULL,
    entry_date     DATE NOT NULL,
    daily_sales    DECIMAL(12,2) NOT NULL,
    daily_expenses DECIMAL(12,2) NOT NULL,
    cash_balance   DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Step 5: Table for money customers owe (receivables)
CREATE TABLE IF NOT EXISTS receivables (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    business_id   INT NOT NULL,
    customer_name VARCHAR(100),
    amount        DECIMAL(12,2) NOT NULL,
    due_date      DATE NOT NULL,
    is_paid       BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Step 6: Table where we save calculated stress scores
CREATE TABLE IF NOT EXISTS stress_scores (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    business_id         INT NOT NULL,
    score_date          DATE NOT NULL,
    expense_ratio       DECIMAL(5,2),
    receivables_stress  DECIMAL(5,2),
    cash_buffer_stress  DECIMAL(5,2),
    burn_rate_stress    DECIMAL(5,2),
    sc_lss_score        DECIMAL(5,2),
    risk_level          VARCHAR(20),
    survival_days       INT,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Step 7: Add 3 sample businesses for testing
INSERT INTO businesses (business_name, owner_name, sector) VALUES
    ('Ravi Textile Traders',    'Ravi Kumar',  'Textile'),
    ('Chennai Auto Parts',      'Meena Devi',  'Manufacturing'),
    ('Sri Lakshmi Groceries',   'Suresh S',    'Retail');