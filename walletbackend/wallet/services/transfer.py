from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.contrib.auth import get_user_model
from wallet.models import Transaction, LedgerEntry,Wallet

User = get_user_model()

def transfer_funds(sender, receiver, amount, idempotency_key=None, description=""):

    if sender == receiver:
        raise ValueError("Cannot transfer to yourself")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    if idempotency_key:
        existing = Transaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing

    with transaction.atomic():

        sender_wallet = Wallet.objects.select_for_update().get(user=sender)
        receiver_wallet = Wallet.objects.select_for_update().get(user=receiver)

        if sender_wallet.balance < amount:
            raise ValueError("Insufficient balance")

        # Create transaction
        txn = Transaction.objects.create(
            sender=sender,
            receiver=receiver,
            amount=amount,
            transaction_type='TRANSFER',
            status='PENDING',
            idempotency_key=idempotency_key,
            description=description
        )

        # Update balances (atomic with F expressions)
        sender_wallet.balance = F('balance') - amount
        receiver_wallet.balance = F('balance') + amount

        sender_wallet.save()
        receiver_wallet.save()

        # Refresh to get actual values
        sender_wallet.refresh_from_db()
        receiver_wallet.refresh_from_db()

        # Ledger entries
        LedgerEntry.objects.create(
            wallet=sender_wallet,
            transaction=txn,
            entry_type='DEBIT',
            amount=amount,
            balance_after=sender_wallet.balance
        )

        LedgerEntry.objects.create(
            wallet=receiver_wallet,
            transaction=txn,
            entry_type='CREDIT',
            amount=amount,
            balance_after=receiver_wallet.balance
        )

        txn.status = 'SUCCESS'
        txn.save()

        return txn