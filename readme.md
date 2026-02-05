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

- **Multi-tenant Support:** Separate businesses and users with isolated data
- **Daily Transactions:** Log income and expenses with easy date tracking
- **Smart Categorization:** Organize transactions by type (rent, stock, transport, salaries, other)
- **Financial Insights:** Monthly profit/loss summaries and cash flow comparisons
- **Offline Capability:** React PWA that works without internet connection
- **Export Functionality:** Generate Excel or PDF reports for accounting needs
- **Admin Dashboard:** Business management and user oversight tools

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | Django 5.0+, Django REST Framework, Gunicorn | API development and business logic |
| **Frontend** | React 19.2.4, Vite, Recharts, React DatePicker | User interface and data visualization |
| **Database** | PostgreSQL | Reliable data storage and transactions |
| **Containerization** | Docker, Docker Compose | Consistent deployment across environments |
| **Authentication** | JWT (DRF SimpleJWT) | Secure user authentication |

---

## Project Structure

```
sme-income-expense/
├── backend/
│   ├── core/                    # Django application core
│   │   ├── models.py           # Database models
│   │   ├── serializers.py      # API serializers
│   │   ├── views.py            # API views
│   │   └── admin.py            # Django admin configuration
│   ├── manage.py               # Django management script
│   ├── Dockerfile              # Backend Docker configuration
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable React components
│   │   │   ├── DatePickerRange.jsx  # Date range selector
│   │   │   ├── CashFlowChart.jsx    # Cash flow visualization
│   │   │   └── ProfitIndicator.jsx  # Profit/loss display
│   │   ├── pages/              # Application pages
│   │   │   └── Dashboard.jsx   # Main dashboard page
│   │   ├── api.js              # API communication utilities
│   │   └── App.js              # Main React application
│   ├── package.json            # Frontend dependencies
│   └── Dockerfile              # Frontend Docker configuration
├── docker-compose.yml          # Multi-container orchestration
├── .env                        # Environment configuration
└── README.md                   # Project documentation
```

---

## Getting Started

### Prerequisites

- **Docker & Docker Compose** (for containerized deployment)
- **Node.js 18+** (for local frontend development)
- **Python 3.11+** (for local backend development)
- **Git** (for version control)

### Local Development

#### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/sme-income-expense.git
cd sme-income-expense/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Unix/macOS)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Backend available at:** http://localhost:8000

#### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend available at:** http://localhost:5173

### Docker Deployment

#### Start All Services

```bash
# From project root directory
docker-compose up --build
```

#### Service Endpoints

| Service | URL | Port | Description |
|---------|-----|------|-------------|
| **Frontend** | http://localhost:3000 | 3000 | User interface |
| **Backend API** | http://localhost:8000/api/v1/ | 8000 | REST API endpoints |
| **Admin Interface** | http://localhost:8000/admin/ | 8000 | Django admin panel |
| **PostgreSQL** | localhost | 5432 | Database service |

#### Stop Services

```bash
# Stop and remove containers
docker-compose down

# Stop, remove containers and volumes (data will be lost)
docker-compose down -v
```

---

## API Endpoints

### Authentication

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/v1/token/` | POST | Obtain JWT access and refresh tokens | None |
| `/api/v1/token/refresh/` | POST | Refresh expired access token | None |
| `/api/v1/token/verify/` | POST | Verify token validity | None |

### Transactions

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/v1/expenses/` | GET | List all expenses | JWT Required |
| `/api/v1/expenses/` | POST | Create new expense | JWT Required |
| `/api/v1/expenses/{id}/` | GET | Retrieve specific expense | JWT Required |
| `/api/v1/expenses/{id}/` | PUT | Update expense | JWT Required |
| `/api/v1/expenses/{id}/` | DELETE | Delete expense | JWT Required |
| `/api/v1/incomes/` | GET | List all incomes | JWT Required |
| `/api/v1/incomes/` | POST | Create new income | JWT Required |

### Analytics

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/v1/cashflow/comparison/` | GET | Compare cash flow with previous period | JWT Required |
| `/api/v1/summary/monthly/` | GET | Get monthly profit/loss summary | JWT Required |
| `/api/v1/summary/category/` | GET | Get spending by category | JWT Required |

### Authentication Header Format

```http
Authorization: Bearer <your_jwt_token_here>
```

---

## Frontend Usage

### Dashboard Components

1. **Date Range Selector**
   - Use the calendar picker to select date ranges
   - Presets for common ranges (Today, This Week, This Month, Last Month)
   - Custom date range selection

2. **Cash Flow Chart**
   - Visualize income vs expenses over time
   - Interactive hover details
   - Comparison with previous period

3. **Profit Indicator**
   - Real-time profit/loss calculation
   - Color-coded indicators (green for profit, red for loss)
   - Percentage change display

4. **Transaction Table**
   - View all transactions in selected period
   - Sort by date, amount, or category
   - Filter by transaction type

### Offline Mode

- The application caches data for offline access
- Works as a Progressive Web App (PWA)
- Syncs data when connection is restored

### Export Features

- **Excel Export:** Generate spreadsheet reports
- **PDF Reports:** Create printable financial summaries
- **CSV Download:** Raw data for external analysis

---

## Testing

### Backend Testing

```bash
cd backend

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=core --cov-report=html

# Run specific test module
pytest core/tests/test_models.py

# Run tests with verbosity
pytest -v
```

### Frontend Testing

```bash
cd frontend

# Run unit tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

### Test Coverage Areas

- **Backend:** API endpoints, models, serializers, authentication
- **Frontend:** React components, API integration, user interactions
- **Integration:** End-to-end flow testing

---

## Environment Variables

### Backend Configuration

```env
# Database Configuration
POSTGRES_DB=sme_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Security Configuration
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:3000
```

### Frontend Configuration

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api/v1/
VITE_APP_NAME=SME Expense Tracker
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_OFFLINE_MODE=true
VITE_ENABLE_EXPORT=true
```

### Production Settings

Create a separate `.env.production` file:

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

---

## Contributing

### Development Workflow

1. **Fork the Repository**
   ```bash
   # Click 'Fork' on GitHub
   git clone https://github.com/yourusername/sme-income-expense.git
   cd sme-income-expense
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: Description of your feature"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   # Create PR on GitHub
   ```

### Code Standards

- **Backend:** Follow Django and PEP 8 conventions
- **Frontend:** Use ESLint and Prettier configuration
- **Commits:** Use conventional commit messages
- **Documentation:** Update README and code comments

### Issue Reporting

1. Check existing issues
2. Use the issue template
3. Provide detailed reproduction steps
4. Include screenshots if applicable

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- **Commercial Use:** Permitted
- **Modification:** Permitted
- **Distribution:** Permitted
- **Private Use:** Permitted
- **Liability:** No warranty
- **Notice:** Include copyright and license notice

### Attribution

If you use this project, please include attribution in your documentation or about section.

---

## Support

- **Documentation:** [GitHub Wiki](https://github.com/yourusername/sme-income-expense/wiki)
- **Issues:** [GitHub Issues](https://github.com/yourusername/sme-income-expense/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/sme-income-expense/discussions)

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/) and [React](https://reactjs.org/)
- Icons from [React Icons](https://react-icons.github.io/react-icons/)
- Charts from [Recharts](https://recharts.org/)
- Date handling with [date-fns](https://date-fns.org/)

---

#### Last Updated: February 2024
