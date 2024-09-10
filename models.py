from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Wallet(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    balance=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet"
class Spending(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spending_id = models.AutoField(primary_key=True)  # Unique identifier for spending
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Spending- {self.amount}"
