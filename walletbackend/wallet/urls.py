from django.urls import path
from .views import WalletView,DepositView,TransactionView,TransferAPIView,GetReceipentApiView

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('transfer/', TransferAPIView.as_view(), name='deposit'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
    path('receiver/', GetReceipentApiView.as_view(), name='receiver'),
]