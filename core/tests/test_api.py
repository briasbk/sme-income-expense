import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import User, Business, Category, Expense, Income
from datetime import date

pytestmark = pytest.mark.django_db  # ENABLE DB FOR ALL TESTS


# ===========================
# Fixtures
# ===========================
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def business():
    return Business.objects.create(name="Test Business")


@pytest.fixture
def user(business):
    return User.objects.create_user(
        username="user1",
        password="pass123",
        business=business
    )


@pytest.fixture
def income_category(business):
    return Category.objects.create(
        name="Sales",
        type="income",
        business=business
    )


@pytest.fixture
def expense_category(business):
    return Category.objects.create(
        name="Rent",
        type="expense",
        business=business
    )


@pytest.fixture
def auth_client(api_client, user):
    url = reverse("token_obtain_pair")
    response = api_client.post(
        url,
        {"username": user.username, "password": "pass123"},
        format="json"
    )

    assert response.status_code == 200  # fail fast if auth breaks

    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


# ===========================
# Authentication
# ===========================
def test_login(api_client, user):
    url = reverse("token_obtain_pair")
    response = api_client.post(
        url,
        {"username": user.username, "password": "pass123"},
        format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data


def test_invalid_login(api_client):
    url = reverse("token_obtain_pair")
    response = api_client.post(
        url,
        {"username": "wrong", "password": "wrong"},
        format="json"
    )

    assert response.status_code == 401


# ===========================
# Expense API
# ===========================
def test_create_expense(auth_client, expense_category):
    url = reverse("expenses-list")

    data = {
        "category": expense_category.id,
        "amount": 500.00,
        "date": date.today(),
        "description": "Office rent"
    }

    response = auth_client.post(url, data, format="json")

    assert response.status_code == 201
    assert float(response.data["amount"]) == 500.00


def test_get_expense_list(auth_client, expense_category, user):
    Expense.objects.create(
        business=expense_category.business,
        user=user,
        category=expense_category,
        amount=200,
        date=date.today()
    )

    url = reverse("expenses-list")
    response = auth_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


# ===========================
# Income API
# ===========================
def test_create_income(auth_client, income_category):
    url = reverse("incomes-list")

    data = {
        "category": income_category.id,
        "source": "Product Sale",
        "amount": 1000.00,
        "date": date.today(),
        "description": "Monthly sales"
    }

    response = auth_client.post(url, data, format="json")

    assert response.status_code == 201
    assert float(response.data["amount"]) == 1000.00


def test_get_income_list(auth_client, income_category, user):
    Income.objects.create(
        business=income_category.business,
        user=user,
        category=income_category,
        source="Service",
        amount=300,
        date=date.today()
    )

    url = reverse("incomes-list")
    response = auth_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


# ===========================
# Cashflow API
# ===========================
def test_cashflow_comparison(auth_client, expense_category, income_category, user):
    business = expense_category.business

    Expense.objects.create(
        business=business,
        user=user,
        category=expense_category,
        amount=200,
        date=date.today()
    )

    Income.objects.create(
        business=business,
        user=user,
        category=income_category,
        source="Sale",
        amount=500,
        date=date.today()
    )

    url = reverse("cashflow_comparison")
    response = auth_client.get(url)

    assert response.status_code == 200

    current = response.data["current_period"]
    assert current["total_income"] == 500.0
    assert current["total_expense"] == 200.0
    assert current["profit"] == 300.0


# ===========================
# Multi-Tenant Isolation
# ===========================
def test_multi_tenant_isolation(auth_client, expense_category, user):
    other_business = Business.objects.create(name="Other Biz")
    other_user = User.objects.create_user(
        username="other",
        password="pass123",
        business=other_business
    )

    other_category = Category.objects.create(
        name="Other Expense",
        type="expense",
        business=other_business
    )

    Expense.objects.create(
        business=other_business,
        user=other_user,
        category=other_category,
        amount=999,
        date=date.today()
    )

    url = reverse("expenses-list")
    response = auth_client.get(url)

    assert response.status_code == 200

    amounts = [float(exp["amount"]) for exp in response.data]
    assert 999.0 not in amounts
