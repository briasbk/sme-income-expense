from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, IncomeViewSet, CashFlowComparisonView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('expenses', ExpenseViewSet, basename='expenses')
router.register('incomes', IncomeViewSet, basename='incomes')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/cashflow/comparison/', CashFlowComparisonView.as_view(), name='cashflow_comparison'),
]
