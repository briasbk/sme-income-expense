from rest_framework import serializers
from core.models import Expense, Income, Category


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "category",
            "amount",
            "date",
            "description",
        ]

    def validate_category(self, category):
        request = self.context.get("request")
        user = request.user if request else None

        if not user or not user.business:
            raise serializers.ValidationError("Invalid user context.")

        if category.business != user.business:
            raise serializers.ValidationError(
                "Category does not belong to your business."
            )

        if category.type != "expense":
            raise serializers.ValidationError(
                "Invalid category type for expense."
            )

        return category


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            "id",
            "category",
            "source",
            "amount",
            "date",
            "description",
        ]

    def validate_category(self, category):
        request = self.context.get("request")
        user = request.user if request else None

        if not user or not user.business:
            raise serializers.ValidationError("Invalid user context.")

        if category.business != user.business:
            raise serializers.ValidationError(
                "Category does not belong to your business."
            )

        if category.type != "income":
            raise serializers.ValidationError(
                "Invalid category type for income."
            )

        return category
