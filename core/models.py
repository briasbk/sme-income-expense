from django.db import models
from django.contrib.auth.models import AbstractUser

# ============================
# Business & Users
# ============================
class Business(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.business})"

# ============================
# Categories (Dynamic)
# ============================
class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)

    class Meta:
        unique_together = ('business', 'name', 'type')
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name} ({self.type})"

# ============================
# Expenses
# ============================
class Expense(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'expense'})
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='paid')
    is_recurring = models.BooleanField(default=False)
    recurring_interval = models.CharField(max_length=20, blank=True, null=True)  # e.g., weekly, monthly
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['business', 'date']),
            models.Index(fields=['category', 'date']),
        ]

    def __str__(self):
        return f"{self.category} - {self.amount}"

# ============================
# Income
# ============================
class Income(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'income'})
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['business', 'date']),
            models.Index(fields=['category', 'date']),
        ]

    def __str__(self):
        return f"{self.source} - {self.amount}"
