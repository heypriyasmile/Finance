from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Wallet, Spending
from django.utils import timezone
from datetime import datetime


# Create your views here.

from decimal import Decimal

# finance/views.py

from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from .models import Spending, Wallet

from django.shortcuts import get_object_or_404

# views.py
def delete_spending(request, spending_id):
    # Retrieve the spending instance or return a 404 response if not found
    spending = get_object_or_404(Spending, spending_id=spending_id)

    # Ensure that the user can only delete their own spending
    if spending.user == request.user:
        # Get the wallet associated with the user
        user_wallet = Wallet.objects.get(user=request.user)

        # Update the wallet balance by adding back the spent amount
        user_wallet.balance += spending.amount
        user_wallet.save()

        # Delete the spending instance
        spending.delete()

    return redirect('wallet')




def add_money(request):
    user = request.user

    try:
        # Attempt to get the user's wallet
        user_wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        # If the wallet doesn't exist, create a new one
        user_wallet = Wallet.objects.create(user=user, balance=0)

    if request.method == 'POST':
        amount_str = request.POST.get('amount')

        try:
            amount = Decimal(amount_str)
        except ValueError:
            return HttpResponse("Invalid amount. Please enter a valid number.")

        if amount <= 0:
            return HttpResponse("Invalid amount. Please enter a positive number.")

        # Update the user's wallet balance
        user_wallet.balance += amount
        user_wallet.save()

        return redirect("wallet")

    return render(request, 'add_money.html')


def wallet(request):
   
    # Check if the user is authenticated
    if not request.user.is_authenticated :
        return HttpResponse("No user found")

    try:
        # Assuming there's a foreign key relationship between User and Wallet
        user_wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        # Handle the case where the wallet does not exist for the user
        user_wallet = None

    # Assuming there's a foreign key relationship between User and Spending
    user_spendings = Spending.objects.filter(user=request.user)

    print(user_wallet)
    print(user_spendings)
    return render(request, 'wallet.html', {'user_wallet': user_wallet, 'user_spendings': user_spendings})

def spending(request):

    if request.method=="POST":
        amount=Decimal(request.POST.get('amount'))
        desc=request.POST.get('description')
        user=request.user


        obj=Spending.objects.create(user=user, amount=amount, description=desc, date=timezone.now())
        obj.save()

        user_wallet=Wallet.objects.get(user=user)
        user_wallet.balance-=amount
        user_wallet.save()

        return redirect("wallet")
    return render(request,'spending.html')

def home(request):
    return render(request, "home.html")


def register(request):

    error_message=None
    if request.method == "POST":
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        user_exists = User.objects.filter(username=username).exists()

    
        if user_exists:
            error_message = "Username already exists. Please choose a different username."
            return render(request, 'register.html', {'error_message': error_message})
        else:
            # If username does not exist, create a new user
            user = User.objects.create(first_name=firstname, last_name=lastname, username=username)
            user.set_password(password)
            user.save()
            return render(request, 'login.html')
    return render(request, 'register.html', {'error_message': error_message})

def Login(request):

    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            return render('login.html')
        
        user=authenticate(username=username,password=password)

        if user is None:

            return render('login.html')
        else:

            login(request,user)
            
            return render(request,'welcome.html')

    return render(request,'Login.html')


def LogOut(request):
    logout(request)
    return render(request,'home.html')

def welcome(request):
    return render(request, 'welcome.html',{'username': request.user.username})


