from django.urls import path

from finance.api.views import CategoryDetailView, CategoryListCreateView, TransactionDetailView, TransactionListCreateView, TransactionSummaryView


urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),

    path('transactions/summary/', TransactionSummaryView.as_view(), name='transaction-summary'),
]
