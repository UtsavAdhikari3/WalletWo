from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Wallet,Transaction
from django.db import transaction
from django.db.models import Q
from .serializers import WalletSerializer,DepositSerializer,TransactionSerializer

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = request.user.wallet
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    

class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)

        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            user = request.user

            with transaction.atomic():
                wallet = user.wallet

                wallet.balance += amount
                wallet.save()

                Transaction.objects.create(
                    receiver=user,
                    amount=amount,
                    transaction_type='DEPOSIT',
                    status='SUCCESS'
                )

            return Response({"message": "Deposit successful"})

        return Response(serializer.errors, status=400)
    
class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        transactions = Transaction.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-created_at')

        serializer = TransactionSerializer(
            transactions,
            many=True,
            context={'request': request} 
        )

        return Response(serializer.data)