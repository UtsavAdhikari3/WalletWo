from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')

    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    currency = models.CharField(max_length=10, default='USD')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} Wallet"
    

class Transaction(models.Model):

    TRANSACTION_TYPE_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('TRANSFER', 'Transfer'),
        ('PAYMENT', 'Payment'),
        ('REFUND', 'Refund'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    reference_id = models.CharField(max_length=100, null=True, blank=True)
    idempotency_key = models.CharField(max_length=100, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.status}"
    
class LedgerEntry(models.Model):

    ENTRY_TYPE_CHOICES = [
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='entries')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user} - {self.entry_type} - {self.amount}"