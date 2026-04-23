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
    
from django.contrib.auth import get_user_model
from wallet.services.transfer import transfer_funds
from decimal import Decimal,InvalidOperation
User = get_user_model()

import re

def normalize_phone(phone):
    return re.sub(r'\D', '', phone)




User = get_user_model()

class TransferAPIView(APIView):

    def post(self, request):
        sender = request.user
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")
        idempotency_key = request.data.get("idempotency_key") or request.data.get("reference_id")

        try:
            if not phone_number:
                return Response({"error": "phone_number is required"}, status=400)

            if not amount:
                return Response({"error": "amount is required"}, status=400)

            phone_number = normalize_phone(phone_number)

            receiver = User.objects.get(phone_number=phone_number)

            if sender.id == receiver.id:
                return Response({"error": "Cannot send to yourself"}, status=400)

            try:
                amount = Decimal(amount)
            except (InvalidOperation, TypeError):
                return Response({"error": "Invalid amount"}, status=400)

            txn = transfer_funds(
                sender=sender,
                receiver=receiver,
                amount=amount,
                idempotency_key=idempotency_key
            )

            return Response({
                "message": "Transfer successful",
                "transaction_id": txn.id,
                "receiver": receiver.username
            })

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class GetReceipentApiView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        sender = request.user
        try:
            phone_number = normalize_phone(phone_number)
            receiver = User.objects.get(phone_number=phone_number)

            if sender.id == receiver.id:
                return Response({"error": "Cannot send to yourself"}, status=400)
            
            return Response({
                "username": receiver.username,
                "email": receiver.email
            })
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

class MerchantPaymentAPIView(APIView):

    def post(self, request):
        sender = request.user
        amount = request.data.get("amount")
        reference_id = request.data.get("reference_id")

        try:
            if not reference_id:
                return Response({"error": "reference_id required"}, status=400)

            if not amount:
                return Response({"error": "amount required"}, status=400)

            amount = Decimal(amount)

            receiver = User.objects.get(username="ecom_system")

            with transaction.atomic():
                sender_wallet = Wallet.objects.select_for_update().get(user=sender)

                if sender_wallet.balance < amount:
                    return Response({"error": "Insufficient balance"}, status=400)

                txn = transfer_funds(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    idempotency_key=reference_id
                )

            import requests
            try:
                requests.post(
                    "http://localhost:8001/api/payment/confirm_payment/",
                    json={
                        "reference_id": reference_id,
                        "success": True,
                        "transaction_id": str(txn.id),
                    },
                    timeout=3
                )
            except Exception as notify_error:
                print("Ecom notify failed:", notify_error)

            return Response({
                "message": "Payment successful",
                "transaction_id": txn.id
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)