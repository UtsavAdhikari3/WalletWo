from django.urls import path
from .views import WalletView,DepositView,TransactionView,TransferAPIView,GetReceipentApiView,MerchantPaymentAPIView

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('transfer/', TransferAPIView.as_view(), name='transfer'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
    path('transfer_merchant/', MerchantPaymentAPIView.as_view(), name='merchant_transfer'),
    path('receiver/', GetReceipentApiView.as_view(), name='receiver'),
]