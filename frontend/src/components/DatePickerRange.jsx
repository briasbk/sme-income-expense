import React from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

export default function DatePickerRange({ startDate, endDate, onChange }) {
  return (
    <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
      <div>
        <label>Start Date:</label>
        <DatePicker
          selected={startDate}
          onChange={(date) => onChange(date, endDate)}
          dateFormat="yyyy-MM-dd"
        />
      </div>
      <div>
        <label>End Date:</label>
        <DatePicker
          selected={endDate}
          onChange={(date) => onChange(startDate, date)}
          dateFormat="yyyy-MM-dd"
        />
      </div>
    </div>
  );
}
