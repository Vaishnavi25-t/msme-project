import React from 'react';
 
// ============================================================
// ResultCard.jsx
// Shows the LSS score, risk level, alert message,
// and all 5 metric cards (ER, RS, CBS, BRS, Survival Days)
// ============================================================
 
const RISK_COLORS = {
  low:    { text: '#16a34a', bg: '#dcfce7' },
  medium: { text: '#d97706', bg: '#fef9c3' },
  high:   { text: '#dc2626', bg: '#fee2e2' },
};
 
function getRiskLevel(label) {
  const l = (label || '').toLowerCase();
  if (l === 'low')    return 'low';
  if (l === 'medium') return 'medium';
  return 'high';
}
 
export default function ResultCard({ result }) {
  const level  = getRiskLevel(result.risk_label);
  const colors = RISK_COLORS[level];
 
  const SECTOR_NAMES = {
    Retail: 'Retail', Manufacturing: 'Manufacturing',
    Wholesale: 'Wholesale', Food_Beverage: 'Food & Beverage', Textile: 'Textile',
  };
 
  const metrics = [
    { label: 'Expense Ratio',       value: (result.expense_ratio      ?? '--') + '%' },
    { label: 'Receivables Stress',  value: (result.receivables_stress ?? '--') + '%' },
    { label: 'Cash Buffer Stress',  value: (result.cash_buffer_stress ?? '--') + '%' },
    { label: 'Burn Rate Stress',    value: (result.burn_rate_stress   ?? '--') + '%' },
    { label: 'Survival Days',       value: result.survival_days >= 999 ? 'Stable' : (result.survival_days ?? '--') + ' days' },
  ];
 
  return (
    <>
      {/* Main score card */}
      <div style={styles.gaugeCard}>
        <h2 style={styles.gaugeTitle}>Liquidity Stress Score (SC-LSS)</h2>
 
        {/* Big score number */}
        <div style={{ ...styles.score, color: colors.text }}>
          {result.sc_lss_score ?? result.lss_score ?? '--'}
        </div>
 
        {/* Risk badge */}
        <div style={{ ...styles.badge, background: colors.bg, color: colors.text }}>
          {level === 'low' ? 'Low Risk' : level === 'medium' ? 'Medium Risk' : 'High Risk'}
        </div>
 
        {/* Sector info */}
        {result.weights_used && (
          <div style={styles.sectorTag}>
            Sector: {SECTOR_NAMES[result.sector] || result.sector} &nbsp;|&nbsp;
            Weights — ER: {result.weights_used.ER * 100}%
            &nbsp; RS: {result.weights_used.RS * 100}%
            &nbsp; CBS: {result.weights_used.CBS * 100}%
            &nbsp; BRS: {result.weights_used.BRS * 100}%
          </div>
        )}
 
        {/* SC-LSS vs generic difference */}
        {result.lss_difference != null && (
          <div style={styles.diffTag}>
            SC-LSS vs generic score: {result.lss_difference >= 0 ? '+' : ''}{result.lss_difference}
          </div>
        )}
 
        {/* Alert message */}
        <div style={{ ...styles.alert, background: colors.bg, color: colors.text }}>
          {result.alert_message}
        </div>
      </div>
 
      {/* Metric cards row */}
      <div style={styles.metricRow}>
        {metrics.map(m => (
          <div key={m.label} style={styles.metricCard}>
            <div style={styles.metricLabel}>{m.label}</div>
            <div style={{ ...styles.metricValue, color: colors.text }}>{m.value}</div>
          </div>
        ))}
      </div>
    </>
  );
}
 
const styles = {
  gaugeCard:   { background:'white', borderRadius:12, padding:28, textAlign:'center', marginBottom:24, boxShadow:'0 1px 4px rgba(0,0,0,0.07)' },
  gaugeTitle:  { fontSize:15, marginBottom:16, color:'#444', margin:'0 0 16px' },
  score:       { fontSize:72, fontWeight:800, lineHeight:1, marginBottom:8 },
  badge:       { display:'inline-block', padding:'6px 20px', borderRadius:20, fontSize:15, fontWeight:600, marginBottom:8 },
  sectorTag:   { fontSize:12, color:'#888', marginBottom:4 },
  diffTag:     { fontSize:12, color:'#888', marginBottom:10 },
  alert:       { fontSize:14, padding:'12px 20px', borderRadius:8, marginTop:10, lineHeight:1.5 },
  metricRow:   { display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(160px,1fr))', gap:14, marginBottom:24 },
  metricCard:  { background:'white', borderRadius:12, padding:18, textAlign:'center', boxShadow:'0 1px 4px rgba(0,0,0,0.07)' },
  metricLabel: { fontSize:11, color:'#888', textTransform:'uppercase', letterSpacing:'0.05em', marginBottom:6 },
  metricValue: { fontSize:26, fontWeight:700 },
};