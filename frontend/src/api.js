// src/api.js
import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

// Retrieve token from localStorage
const getToken = () => localStorage.getItem("access_token");

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (username, password) => {
  const response = await axios.post(`${API_BASE_URL}/token/`, { username, password });
  localStorage.setItem("access_token", response.data.access);
  localStorage.setItem("refresh_token", response.data.refresh);
  return response.data;
};

export const fetchExpenses = async (params = {}) => {
  const response = await api.get("/expenses/", { params });
  return response.data;
};

export const fetchIncomes = async (params = {}) => {
  const response = await api.get("/incomes/", { params });
  return response.data;
};

export const getCashFlowComparison = async (startDate, endDate) => {
  const response = await api.get("/cashflow/comparison/", {
    params: { start_date: startDate, end_date: endDate },
  });
  return response.data;
};
