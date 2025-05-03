from finance.models import Category, Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from utils.paginator import CustomPaginator
from .serializers import CategorySerializer, TransactionSerializer
from django.db.models import Sum

class CategoryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
            categories = Category.objects.filter(user=request.user)
            paginator = CustomPaginator()
            paginated_categories = paginator.paginate_queryset(categories, request)

            if not paginated_categories:
                return Response({
                    "success": True,
                    "message": "No data",
                    "count": 0,
                    "data": []
                })

            serializer = CategorySerializer(paginated_categories, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request):
            name = request.data.get('name')

            if Category.objects.filter(name=name).exists():
                return Response({
                    "success": False,
                    "message": "Category with this name already exists.",
                    "errors": {"name": ["This category already exists."]}
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = CategorySerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Category created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "success": False,
                "message": "Failed to create category",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Category.objects.get(pk=pk, user=user)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk, request.user)
        if not category:
            return Response({"success": False, "message": "Category not found"}, status=404)
        serializer = CategorySerializer(category)
        return Response({"success": True, "message": "Category retrieved", "data": serializer.data})

    def put(self, request, pk):
        category = self.get_object(pk, request.user)
        if not category:
            return Response({"success": False, "message": "Category not found"}, status=404)

        # Check for existing category with the same name but a different ID
        new_name = request.data.get('name')
        if new_name and Category.objects.filter(name=new_name).exclude(id=category.id).exists():
            return Response({
                "success": False,
                "message": "Category with this name already exists.",
                "errors": {"name": ["This category name already exists."]}
            }, status=400)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Category updated",
                "data": serializer.data
            })

        return Response({
            "success": False,
            "message": "Failed to update",
            "errors": serializer.errors
        }, status=400)


    def delete(self, request, pk):
        category = self.get_object(pk, request.user)
        if not category:
            return Response({"success": False, "message": "Category not found"}, status=404)
        category.delete()
        return Response({"success": True, "message": "Category deleted"}, status=204)

class TransactionListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        transaction_type = request.query_params.get("transaction_type")
        category = request.query_params.get("category")
        date = request.query_params.get("date")

        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)
        if category:
            transactions = transactions.filter(category__id=category)
        if date:
            transactions = transactions.filter(date=date)

        paginator = CustomPaginator()
        paginated_transactions = paginator.paginate_queryset(transactions, request)

        serializer = TransactionSerializer(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        # Check if similar transaction already exists
        if Transaction.objects.filter(
            user=request.user,
            amount=request.data.get('amount'),
            description=request.data.get('description'),
            date=request.data.get('date')
        ).exists():
            return Response({
                "success": False,
                "message": "Transaction already exists with the same details"
            }, status=400)

        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Transaction created successfully",
                "data": serializer.data
            }, status=201)
        return Response({
            "success": False,
            "message": "Failed to create transaction",
            "errors": serializer.errors
        }, status=400)



class TransactionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Transaction.objects.get(pk=pk, user=user)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if not transaction:
            return Response({"success": False, "message": "Transaction not found"}, status=404)
        serializer = TransactionSerializer(transaction)
        return Response({"success": True, "message": "Transaction retrieved", "data": serializer.data})

    def put(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if not transaction:
            return Response({"success": False, "message": "Transaction not found"}, status=404)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Transaction updated", "data": serializer.data})
        return Response({"success": False, "message": "Failed to update", "errors": serializer.errors}, status=400)

    def delete(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if not transaction:
            return Response({"success": False, "message": "Transaction not found"}, status=404)
        transaction.delete()
        return Response({"success": True, "message": "Transaction deleted"}, status=204)

class TransactionSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        income = transactions.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
        expenses = transactions.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0
        net = income - expenses

        return Response({
            "success": True,
            "message": "Summary retrieved successfully",
            "data": {
                "total_income": income,
                "total_expense": expenses,
                "net_balance": net
            }
        })
