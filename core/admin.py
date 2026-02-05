from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import date
from core.models import User, Business, Category, Expense, Income

pytestmark = pytest.mark.django_db

# ============================
# Business Admin
# ============================
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

# ============================
# User Admin
# ============================
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'business', 'is_staff', 'is_active')
    list_filter = ('business', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('business',)}),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)

# ============================
# Category Admin
# ============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'business')
    list_filter = ('business', 'type')
    search_fields = ('name',)
    ordering = ('business', 'type', 'name')

# ============================
# Expense Admin
# ============================
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'user', 'category', 'amount', 'status', 'date', 'is_recurring')
    list_filter = ('business', 'category', 'status', 'date', 'is_recurring')
    search_fields = ('description',)
    ordering = ('-date', 'business')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('business', 'user', 'category', 'amount', 'status', 'date')
        }),
        ('Optional Info', {
            'fields': ('description', 'receipt', 'is_recurring', 'recurring_interval')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

# ============================
# Income Admin
# ============================
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'user', 'category', 'source', 'amount', 'date')
    list_filter = ('business', 'category', 'date')
    search_fields = ('source', 'description')
    ordering = ('-date', 'business')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('business', 'user', 'category', 'source', 'amount', 'date')
        }),
        ('Optional Info', {
            'fields': ('description', 'receipt')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
