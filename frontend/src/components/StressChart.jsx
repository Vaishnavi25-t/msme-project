import React from 'react';

const StressChart = ({ data }) => {
  return (
    <div>
      <h3>Stress Chart</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default StressChart;