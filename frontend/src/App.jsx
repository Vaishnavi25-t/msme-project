import React, { useState } from 'react';
import InputForm  from './components/InputForm';
import ResultCard from './components/ResultCard';
import StressChart from './components/StressChart';
 
// ============================================================
// App.jsx  —  Main component
// Holds state, calls Java backend, passes data to children
// ============================================================
 
export default function App() {
  const [result,  setResult]  = useState(null);   // stores API response
  const [loading, setLoading] = useState(false);  // shows "Analyzing..." text
  const [error,   setError]   = useState('');     // shows error message
 
  // Called when user clicks "Analyze Now"
  async function handleAnalyze(formData) {
    setLoading(true);
    setError('');
    setResult(null);
 
    try {
      // Send data to Java backend on port 8082
      const response = await fetch('http://localhost:8082/api/analyze', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(formData),
      });
 
      const data = await response.json();
 
      if (!response.ok || data.error) {
        setError(data.error || 'Something went wrong.');
        return;
      }
 
      setResult(data);
    } catch {
      setError(
        'Cannot reach the backend.\n' +
        'Make sure Python (port 5000) and Java (port 8080) are running.'
      );
    } finally {
      setLoading(false);
    }
  }
 
  return (
    <div style={styles.page}>
      {/* Header */}
      <header style={styles.header}>
        <h1 style={styles.headerTitle}>MSME Working Capital Stress Analyzer</h1>
        <span style={styles.headerSub}>Sector-Calibrated Liquidity Risk Dashboard</span>
      </header>
 
      <div style={styles.container}>
        {/* Input Form */}
        <InputForm onSubmit={handleAnalyze} loading={loading} />
 
        {/* Error message */}
        {error && (
          <div style={styles.errorBox}>
            <strong>Error:</strong> {error}
          </div>
        )}
 
        {/* Results */}
        {result && (
          <>
            <ResultCard result={result} />
            <StressChart result={result} />
          </>
        )}
      </div>
    </div>
  );
}
 
const styles = {
  page: {
    fontFamily: "'Segoe UI', sans-serif",
    background: '#f0f2f5',
    minHeight:  '100vh',
    color:      '#1a1a2e',
  },
  header: {
    background:     '#1a1a2e',
    color:          'white',
    padding:        '18px 32px',
    display:        'flex',
    alignItems:     'center',
    justifyContent: 'space-between',
  },
  headerTitle: { fontSize: 20, fontWeight: 600, margin: 0 },
  headerSub:   { fontSize: 13, color: '#a0a8c0' },
  container: {
    maxWidth: 1100,
    margin:   '0 auto',
    padding:  '24px 16px',
  },
  errorBox: {
    background:   '#fee2e2',
    color:        '#991b1b',
    padding:      '14px 18px',
    borderRadius: 10,
    marginBottom: 20,
    whiteSpace:   'pre-line',
  },
};