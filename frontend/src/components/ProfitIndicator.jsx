import React from 'react';

export default function ProfitIndicator({ currentProfit, previousProfit }) {
  const change = previousProfit ? ((currentProfit - previousProfit) / previousProfit) * 100 : 0;
  return (
    <div>
      <h3>Profit: {currentProfit.toFixed(2)}</h3>
      <p>
        Change from previous period: <strong>{change.toFixed(2)}%</strong>
      </p>
    </div>
  );
}
