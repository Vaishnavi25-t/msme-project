import React, { useState } from 'react';
 
// ============================================================
// InputForm.jsx
// The form where the user enters daily financial data
// When "Analyze Now" is clicked, it calls onSubmit(formData)
// ============================================================
 
const SECTORS = [
  { value: '',              label: '-- Select Sector --' },
  { value: 'Retail',        label: 'Retail' },
  { value: 'Manufacturing', label: 'Manufacturing' },
  { value: 'Wholesale',     label: 'Wholesale' },
  { value: 'Food_Beverage', label: 'Food & Beverage' },
  { value: 'Textile',       label: 'Textile' },
];
 
const FIELDS = [
  { id: 'daily_sales',          label: 'Daily Sales (₹)',          placeholder: 'e.g. 15000' },
  { id: 'daily_expenses',       label: 'Daily Expenses (₹)',        placeholder: 'e.g. 12000' },
  { id: 'cash_balance',         label: 'Current Cash Balance (₹)', placeholder: 'e.g. 80000' },
  { id: 'total_receivables',    label: 'Total Receivables (₹)',     placeholder: 'e.g. 50000' },
  { id: 'overdue_receivables',  label: 'Overdue Receivables (₹)',   placeholder: 'e.g. 20000' },
  { id: 'avg_delay_days',       label: 'Avg Payment Delay (days)',  placeholder: 'e.g. 30'    },
  { id: 'monthly_expenses',     label: 'Monthly Expenses (₹)',      placeholder: 'e.g. 360000'},
];
 
export default function InputForm({ onSubmit, loading }) {
  // Store form values in state
  const [values, setValues] = useState({
    sector:             '',
    daily_sales:        '',
    daily_expenses:     '',
    cash_balance:       '',
    total_receivables:  '',
    overdue_receivables:'',
    avg_delay_days:     '',
    monthly_expenses:   '',
  });
 
  function handleChange(e) {
    setValues({ ...values, [e.target.name]: e.target.value });
  }
 
  function handleSubmit() {
    // Validate sector
    if (!values.sector) {
      alert('Please select a Business Sector.');
      return;
    }
    // Validate all numeric fields
    for (const field of FIELDS) {
      const val = parseFloat(values[field.id]);
      if (isNaN(val) || val < 0) {
        alert(`Please enter a valid number for: ${field.label}`);
        return;
      }
    }
    // Build the data object to send
    const formData = {
      sector:              values.sector,
      daily_sales:         parseFloat(values.daily_sales),
      daily_expenses:      parseFloat(values.daily_expenses),
      cash_balance:        parseFloat(values.cash_balance),
      total_receivables:   parseFloat(values.total_receivables),
      overdue_receivables: parseFloat(values.overdue_receivables),
      avg_delay_days:      parseFloat(values.avg_delay_days),
      monthly_expenses:    parseFloat(values.monthly_expenses),
    };
    onSubmit(formData);
  }
 
  return (
    <div style={styles.card}>
      <h2 style={styles.title}>Enter Daily Financial Data</h2>
 
      <div style={styles.grid}>
        {/* Sector Dropdown */}
        <div style={styles.group}>
          <label style={styles.label}>Business Sector</label>
          <select
            name="sector"
            value={values.sector}
            onChange={handleChange}
            style={styles.input}
          >
            {SECTORS.map(s => (
              <option key={s.value} value={s.value}>{s.label}</option>
            ))}
          </select>
        </div>
 
        {/* Numeric Fields */}
        {FIELDS.map(f => (
          <div key={f.id} style={styles.group}>
            <label style={styles.label}>{f.label}</label>
            <input
              type="number"
              name={f.id}
              value={values[f.id]}
              onChange={handleChange}
              placeholder={f.placeholder}
              min="0"
              style={styles.input}
            />
          </div>
        ))}
      </div>
 
      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{ ...styles.button, opacity: loading ? 0.6 : 1 }}
      >
        {loading ? 'Analyzing...' : 'Analyze Now'}
      </button>
    </div>
  );
}
 
const styles = {
  card:   { background:'white', borderRadius:12, padding:24, marginBottom:24, boxShadow:'0 1px 4px rgba(0,0,0,0.07)' },
  title:  { fontSize:16, marginBottom:18, color:'#1a1a2e', margin:'0 0 18px' },
  grid:   { display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(200px, 1fr))', gap:14 },
  group:  { display:'flex', flexDirection:'column' },
  label:  { fontSize:12, color:'#666', marginBottom:5, fontWeight:500 },
  input:  { padding:'10px 12px', border:'1px solid #dde1ea', borderRadius:8, fontSize:14, outline:'none', background:'white' },
  button: { marginTop:18, background:'#4f46e5', color:'white', border:'none', padding:'12px 32px', borderRadius:8, fontSize:15, fontWeight:600, cursor:'pointer' },
};