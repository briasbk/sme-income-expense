import React, { useState, useEffect } from 'react';
import DatePickerRange from '../components/DatePickerRange';
import CashFlowChart from '../components/CashFlowChart';
import ProfitIndicator from '../components/ProfitIndicator';
import { getCashFlowComparison } from '../api';

export default function Dashboard() {
  const [startDate, setStartDate] = useState(new Date(new Date().setDate(1))); // first of month
  const [endDate, setEndDate] = useState(new Date()); // today
  const [data, setData] = useState(null);

  const fetchData = async (start, end) => {
    try {
      const response = await getCashFlowComparison(
        start.toISOString().split('T')[0],
        end.toISOString().split('T')[0]
      );
      setData(response.data);
      // Save to localStorage for offline
      localStorage.setItem('lastCashFlow', JSON.stringify(response.data));
    } catch (err) {
      console.error(err);
      // Load offline data
      const offline = localStorage.getItem('lastCashFlow');
      if (offline) setData(JSON.parse(offline));
    }
  };

  useEffect(() => {
    fetchData(startDate, endDate);
  }, [startDate, endDate]);

  const handleDateChange = (start, end) => {
    setStartDate(start);
    setEndDate(end);
  };

  if (!data) return <p>Loading...</p>;

  const chartData = [
    {
      name: 'Income',
      current: data.current_period.total_income,
      previous: data.previous_period.total_income,
    },
    {
      name: 'Expenses',
      current: data.current_period.total_expense,
      previous: data.previous_period.total_expense,
    },
  ];

  return (
    <div>
      <h2>Cash Flow Dashboard</h2>
      <DatePickerRange
        startDate={startDate}
        endDate={endDate}
        onChange={handleDateChange}
      />
      <CashFlowChart data={chartData} />
      <ProfitIndicator
        currentProfit={data.current_period.profit}
        previousProfit={data.previous_period.profit}
      />
    </div>
  );
}
