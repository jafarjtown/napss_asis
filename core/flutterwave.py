import requests
from django.conf import settings

FLUTTERWAVE_BASE_URL = "https://api.flutterwave.com/v3"

def buy_data(phone_number, network, amount):
    """
    Function to purchase data via Flutterwave's Bills Payment API.
    
    :param phone_number: The recipient's phone number.
    :param network: The network provider (e.g., "MTN", "AIRTEL").
    :param amount: The amount of data in NGN.
    :return: Response from the Flutterwave API.
    """
    url = f"{FLUTTERWAVE_BASE_URL}/bills"
    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "country": "NG",  # Nigeria
        "customer": phone_number,
        "amount": amount,
        "type": network.lower(),  # Example: "mtn" or "airtel"
        "reference": "data-" + str(phone_number),
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()