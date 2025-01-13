from django.shortcuts import render
from .models import Wallet
# Create your views here.

def wallet(request):
  user_wallet, _ = Wallet.objects.get_or_create(owner=request.user)
  return render(request, 'wallet/index.html', {'wallet':user_wallet})