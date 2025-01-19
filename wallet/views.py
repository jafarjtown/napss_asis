from django.shortcuts import render, redirect
from .models import Wallet, GeneratedLink
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from core import monnify, flutterwave

import datetime
import hmac
import hashlib
import json

@csrf_exempt
def monnify_webhook(request):
    if request.method == "POST":
        try:
            # Step 1: Validate the request signature
            request_body = request.body
            signature = request.headers.get("monnify-signature")
            calculated_signature = hmac.new(
                settings.MONNIFY_SECRET_KEY.encode(),
                request_body,
                hashlib.sha512
            ).hexdigest()

            if signature != calculated_signature:
                return JsonResponse({"status": "error", "message": "Invalid signature"}, status=400)

            # Step 2: Parse the request data
            data = json.loads(request_body)
            if data.get("eventType") == "SUCCESSFUL_TRANSACTION":
                payment_details = data.get("eventData")

                # Extract relevant details
                account_reference = payment_details.get("accountReference")
                amount_paid = float(payment_details.get("amountPaid"))
                customer_name = payment_details.get("customerName")
                transaction_reference = payment_details.get("transactionReference")
                payment_date = payment_details.get("paidOn")

                # Step 3: Update the user's wallet
                from .models import Wallet  # Ensure you import your wallet model
                wallet = Wallet.objects.filter(account_reference=account_reference).first()
                if wallet:
                    wallet.balance += amount_paid
                    wallet.save()

                    # Optionally log the transaction (e.g., save to a transaction model)
                    wallet.transactions.create(
                        amount=amount_paid,
                        reference=transaction_reference,
                        date=payment_date,
                        customer_name=customer_name,
                    )

                return JsonResponse({"status": "success", "message": "Payment processed successfully"}, status=200)
            else:
                return JsonResponse({"status": "ignored", "message": "Event type not relevant"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
    
    

def wallet(request):
  if request.method == 'POST':
    nin = request.POST.get('nin')
    user_wallet, _ = Wallet.objects.get_or_create(user=request.user, nin=nin)
    
  return render(request, 'wallet/index.html')

def fund_wallet(request):
  pass

def generate_wallet(request):
    user = request.user
    if request.method == 'POST':
        try:
            # Generate a unique account reference (e.g., using timestamp)
            account_reference = str(datetime.datetime.now().timestamp())

            # Call the Monnify API to generate a virtual account
            response = monnify.create_virtual_account(
                user.get_full_name(),
                user.email,
                account_reference,
                user.wallet.nin
            )
            print(response)
            # Check if the API response is successful
            if response.get('requestSuccessful') and response.get('responseBody'):
                bank_name = response['responseBody']['bankName']
                account_number = response['responseBody']['accountNumber']
                account_name = response['responseBody']['accountName']

                # Update the user's wallet with the generated account details
                user_wallet = user.wallet
                user_wallet.account_name = account_name
                user_wallet.account_number = account_number
                user_wallet.bank_name = bank_name
                user_wallet.save()

                messages.success(request, "Virtual account generated successfully.")
            else:
                messages.error(request, "Failed to generate virtual account. Please try again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect('wallet:index')

def buy_data(request):
  return render(request, 'wallet/data.html')


def purchase_data_with_wallet(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        network = request.POST.get("network")
        amount = float(request.POST.get("amount"))

        user_wallet = request.user.wallet

        # Check if the user has enough funds in their wallet
        if user_wallet.balance < amount:
            messages.error(request, "Insufficient wallet balance. Please fund your wallet.")
            return redirect("wallet:buy_data")

        try:
            # Deduct the amount from the user's wallet
            user_wallet.balance -= amount
            user_wallet.save()

            # Use Flutterwave API to process the data purchase
            response = flutterwave.buy_data(phone_number, network, amount)
            if response.get("status") == "success":
                messages.success(request, "Data purchase successful!")
            else:
                # Refund the wallet if the transaction fails
                user_wallet.balance += amount
                user_wallet.save()
                messages.error(request, f"Data purchase failed: {response.get('message')}")

        except Exception as e:
            # Handle errors and refund the wallet if necessary
            user_wallet.balance += amount
            user_wallet.save()
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect("wallet:buy_data")
    return redirect("wallet:buy_data")

def purchase_airtime_with_wallet(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        network = request.POST.get("network")
        amount = float(request.POST.get("amount"))

        user_wallet = request.user.wallet

        # Check if the user has enough funds in their wallet
        if user_wallet.balance < amount:
            messages.error(request, "Insufficient wallet balance. Please fund your wallet.")
            return redirect("wallet:buy_airtime")

        try:
            # Deduct the amount from the user's wallet
            user_wallet.balance -= amount
            user_wallet.save()

            # Use Flutterwave API to process the data purchase
            response = flutterwave.buy_data(phone_number, network, amount)
            if response.get("status") == "success":
                messages.success(request, "Airtime purchase successful!")
            else:
                # Refund the wallet if the transaction fails
                user_wallet.balance += amount
                user_wallet.save()
                messages.error(request, f"Airtime purchase failed: {response.get('message')}")

        except Exception as e:
            # Handle errors and refund the wallet if necessary
            user_wallet.balance += amount
            user_wallet.save()
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect("wallet:buy_airtime")
    return redirect("wallet:buy_airtime")
    
def buy_airtime(request):
  return render(request, 'wallet/airtime.html')

def generate_link(request):
  context = {}
  if request.method == 'POST':
    
    network = request.POST.get('network')
    name = request.POST.get('name')
    link_type = request.POST.get('type')
    slot = request.POST.get('slot')
    if link_type == 'airtime':
      amount = request.POST.get('airtime-amount')
    else:
      amount = request.POST.get('data-amount')
    expense = int(amount) * int(slot)
    link = GeneratedLink.objects.create(name=name, network=network, link_type=link_type, slot=slot, available_slot=slot, amount=amount)
    context['link'] = link
  return render(request, 'wallet/generate.html', context)

def use_generated_link(request, id):
  context = {}
  link = GeneratedLink.objects.get(id=id)
  if request.method == 'POST':
    if link.available_slot == 0:
      messages.error(request, 'Slot not available.')
      return redirect('wallet:generated_link', id)
    number = request.POST.get('number')
    amount = link.amount 
    network = link.network
    if link.beneficiaries.filter(phone_number=number).exists():
      messages.error(request, 'You already benefit, let others do.')
      return redirect('wallet:generated_link', id)
      
    link.available_slot -= 1 
    link.beneficiaries.create(phone_number=number)
    link.save()
    messages.success(request, 'Transanction successful')
    return redirect('wallet:generated_link', id)
  context['link'] = link
  
  return render(request, 'wallet/generated_link.html', context)


def _generate_wallet(request):
  user = request.user
  if request.method == 'POST':
    #response = monnify.create_virtual_account(user.get_full_name(), user.email, str(datetime.datetime.now()), user.wallet.nin)
    bank_name = 'Opay'
    account_number = '7080332077'
    account_name = 'Jafaru Idris'
    user_wallet = user.wallet
    
    user_wallet.account_name = account_name
    user_wallet.account_number = account_number
    user_wallet.bank_name = bank_name
    user_wallet.save()
  return redirect('wallet:index')