# SME Expense & Cash Flow Tracker

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-19.2.4-blue)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-green)](https://github.com/)

A multi-tenant, cloud-ready, offline-capable expense and cash flow tracker for small businesses. Designed for non-accountants, this application provides an intuitive way to log income and expenses, visualize cash flow, and generate monthly summaries.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Project Structure](#project-structure)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Local Development](#local-development)  
  - [Docker Deployment](#docker-deployment)  
- [API Endpoints](#api-endpoints)  
- [Frontend Usage](#frontend-usage)  
- [Testing](#testing)  
- [Environment Variables](#environment-variables)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- Multi-tenant support: separate businesses and users  
- Daily income and expense logging  
- Categorization of transactions (rent, stock, transport, salaries, other)  
- Monthly profit/loss summary and cash flow comparison  
- Offline-capable React frontend (PWA)  
- Export reports to Excel or PDF  
- Admin dashboard for business management  

---

## Tech Stack

- **Backend:** Django, Django REST Framework, Gunicorn  
- **Frontend:** React, Vite, Recharts (charts), React DatePicker  
- **Database:** PostgreSQL  
- **Containerization:** Docker, Docker Compose  
- **Other:** JWT Authentication (DRF SimpleJWT)  

---

## Project Structure
sme-income-expense/
├── backend/
│ ├── core/ # Django app with models, serializers, views
│ ├── manage.py
│ ├── Dockerfile
│ └── requirements.txt
├── frontend/
│ ├── src/
│ │ ├── components/ # React components (DatePickerRange, CashFlowChart, ProfitIndicator)
│ │ ├── pages/ # React pages (Dashboard)
│ │ ├── api.js # API utilities
│ │ └── App.js
│ ├── package.json
│ └── Dockerfile
├── docker-compose.yml
├── .env
└── README.md


---

## Getting Started

### Prerequisites

- Docker & Docker Compose  
- Node.js (if running frontend locally without Docker)  
- Python 3.11+  

---

### Local Development (without Docker)

1. **Backend**  
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


Backend available at: http://localhost:8000

Frontend

cd frontend
npm install
npm run dev


Frontend available at: http://localhost:5173 (Vite default port)

Docker Deployment (Recommended)

Build and start all services

docker-compose up --build


Access Services

Frontend: http://localhost:3000

Backend API: http://localhost:8000/api/v1/

PostgreSQL: localhost:5432

Stop Services

docker-compose down

API Endpoints
Endpoint	Method	Description
/api/v1/token/	POST	Obtain JWT token
/api/v1/token/refresh/	POST	Refresh JWT token
/api/v1/expenses/	GET/POST	List or create expenses
/api/v1/incomes/	GET/POST	List or create incomes
/api/v1/cashflow/comparison/	GET	Compare cash flow with previous period

All endpoints require JWT authentication. Include the token in headers:

Authorization: Bearer <token>

Frontend Usage

Dashboard Page: displays charts for income vs expenses, and profit indicators

Date Picker: select a date range to filter transactions

Offline Mode: PWA caching allows offline viewing of previous data

API Configuration: frontend/src/api.js handles all backend calls

Testing

The project uses pytest and DRF test client.
To run backend tests:

cd backend
pytest

Environment Variables

Example .env:

POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DB=sme_db
DJANGO_SECRET_KEY=supersecretkey
DJANGO_DEBUG=1


Keep .env out of version control

Used by backend and Docker Compose

Contributing

Fork the repository

Create a branch: git checkout -b feature/my-feature

Make changes and commit: git commit -m "Add new feature"

Push to branch: git push origin feature/my-feature

Open a Pull Request

License

This project is licensed under the MIT License.


----