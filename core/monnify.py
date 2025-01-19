import requests, base64
from django.conf import settings

BASE_URL = "https://sandbox.monnify.com/api/v1"  # Use live URL for production
API_KEY = settings.MONNIFY_API_KEY
SECRET_KEY = settings.MONNIFY_SECRET_KEY
CONTRACT_CODE = settings.MONNIFY_CONTRACT_CODE

def get_access_token():
    url = f"{BASE_URL}/auth/login"
    credentials = f"{settings.MONNIFY_API_KEY}:{settings.MONNIFY_SECRET_KEY}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
    }
    response = requests.post(url, headers=headers)
    #print("Response Status:", response.status_code)
    #print("Response Body:", response.json())  # Log the full response for debugging
    
    response_data = response.json()
    if response.status_code == 200:
        return response_data["responseBody"]["accessToken"]
    else:
        raise Exception(f"Error fetching access token: {response_data['responseMessage']}")


def create_virtual_account(customer_name, customer_email, account_reference, customer_nin):
    try:
        access_token = get_access_token()
        url = f"{BASE_URL}/bank-transfer/reserved-accounts"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "accountReference": account_reference,
            "accountName": customer_name,
            "currencyCode": "NGN",
            "contractCode": CONTRACT_CODE,
            "customerEmail": customer_email,
            "incomeSplitConfig": [],
            "nin": customer_nin
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
        
  
  

def transfer_to_flutterwave(account_number, bank_code, amount, narration="Transfer to Flutterwave Wallet"):
    """
    Transfer funds from Monnify wallet to a Flutterwave wallet.

    :param account_number: The Flutterwave wallet account number.
    :param bank_code: The bank code for Flutterwave wallet (e.g., "044" for Access Bank).
    :param amount: Amount to transfer.
    :param narration: Narration for the transaction.
    :return: Response from Monnify API.
    """
    # Authenticate with Monnify
    access_token = get_access_token()
    if not access_token:
        raise Exception("Failed to authenticate with Monnify")

    # Transfer funds
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "amount": amount,
        "destinationBankCode": bank_code,
        "destinationAccountNumber": account_number,
        "narration": narration,
        "reference": "TRX-" + str(account_number),
    }

    response = requests.post(f"{BASE_URL}/disbursements/single", json=payload, headers=headers)
    return response.json()
  
  
  