import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function CashFlowChart({ data }) {
  // Data example: [{ name: 'Income', current: 12000, previous: 11000 }, ...]
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="current" fill="#4caf50" name="Current Period" />
        <Bar dataKey="previous" fill="#ff9800" name="Previous Period" />
      </BarChart>
    </ResponsiveContainer>
  );
}
