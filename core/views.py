
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseSerializer, IncomeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from datetime import datetime, timedelta, date
from .models import Expense, Income
from dateutil.relativedelta import relativedelta
class ExpenseViewSet(ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
    # Enforce business filtering for multi-tenant safety
        return super().get_queryset().filter(business=self.request.user.business)


    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business, user=self.request.user)

class IncomeViewSet(ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
    # Enforce business filtering for multi-tenant safety
        return super().get_queryset().filter(business=self.request.user.business)


    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business, user=self.request.user)

class CashFlowComparisonView(APIView):
    """
    Returns total income, total expenses, and profit/loss for a selected date range.
    Also returns same metrics for the previous period (same length).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = date.today()

        # Parse query params
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else today.replace(day=1)
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else today
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Ensure start_date <= end_date
        if start_date > end_date:
            return Response({"error": "start_date cannot be after end_date."}, status=400)

        # Compute previous period (same number of days)
        delta_days = (end_date - start_date).days + 1
        prev_end = start_date - timedelta(days=1)
        prev_start = prev_end - timedelta(days=delta_days - 1)

        # Helper function
        def summarize(business, start, end):
            incomes = Income.objects.filter(business=business, date__gte=start, date__lte=end).aggregate(total_income=Sum('amount'))['total_income'] or 0
            expenses = Expense.objects.filter(business=business, date__gte=start, date__lte=end).aggregate(total_expense=Sum('amount'))['total_expense'] or 0
            return {
                "total_income": float(incomes),
                "total_expense": float(expenses),
                "profit": float(incomes - expenses),
            }

        current = summarize(user.business, start_date, end_date)
        previous = summarize(user.business, prev_start, prev_end)

        return Response({
            "current_period": {
                "start_date": str(start_date),
                "end_date": str(end_date),
                **current
            },
            "previous_period": {
                "start_date": str(prev_start),
                "end_date": str(prev_end),
                **previous
            }
        })
