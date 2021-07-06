from flask import Blueprint
from flask import current_app
from ..app import create_app
from ..app import login_manager
from ..models import *
from ..decorators import admin_required, moderator_required, permission_required
from sqlalchemy import or_,and_
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
)
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
import requests
import json
import base64
from requests.auth import HTTPBasicAuth
import unicodedata, re, itertools, sys
from datetime import datetime

mpesa = Blueprint("mpesa", __name__, url_prefix="/mpesa")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# *** Authorization Request in Python ***|
base_url = 'http://102.167.16.174'
consumer_key = 'Y029iJrJGeGdOlBKIlhGgJnrL6AAGrtF'
consumer_secret = 'HF2s63AZ5RTw00jT'
business_short_code = '5983411'
lipa_na_mpesa_passkey = ''


# access token
@mpesa.route("/access_token")
def token():
    data = ac_token()
    return data


# register urls
@mpesa.route("/register_urls")
def register():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = { "Authorization ":"Bearer %s" % ac_token()}

    req_body = {
        "ShortCode": "600992",
        "ResponseType": "Completed",
        "ConfirmationURL": base_url + "/confirmation",
        "ValidationURL": base_url + "/validation"
        }

    response_data = requests.post(
        mpesa_endpoint,
        json=req_body,
        headers=headers
        )
    return response_data.json()

@mpesa.route("/c2b/confirm")
def confirm():
    # get data
    data = request.get_json()
    # write to file
    file = open('./confirm.json', 'a')
    file.write(json.dumps(data))
    file.close()

    return {
        "ResultCode":0,
        "ResultDesc": "Accepted"
    }


@mpesa.route("/c2b/validation")
def validate():
    # get data
    data = request.get_json()
    # write to file
    file = open('./confirm.json', 'a')
    file.write(json.dumps(data))
    file.close()

    return {
        "ResultCode":0,
        "ResultDesc": "Accepted"
    }

date = datetime.now()
formatted_time = date.strftime("%Y%m%d%H%M%S")

data_to_encode = business_short_code + lipa_na_mpesa_passkey + formatted_time
encoded_string = base64.b64encode(data_to_encode.encode())
decoded_string = encoded_string.decode('utf-8')

# simulate 
@mpesa.route("/simulate")
def simulate():
    mpesa_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    access_token = ac_token()

    headers = { "Authorization ":"Bearer %s" % ac_token()}

    request_body = {

            "BusinessShortCode":business_short_code,    
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",    
            "Timestamp":formatted_time,    
            "TransactionType": "CustomerPayBillOnline",    
            "Amount":"1",    
            "PartyA":"254708176232",    
            "PartyB":business_short_code,    
            "PhoneNumber":"254708176232",    
            "CallBackURL":"https://darajambili.herokuapp.com/express-payment",    
            "AccountReference":"Test",    
            "TransactionDesc":"Pay Hostel Booking Fee"

            # "BusinessShortCode":business_short_code,    
            # "Password":decoded_string,    
            # "Timestamp":formatted_time,    
            # "TransactionType": "CustomerPayBillOnline",    
            # "Amount":"1",    
            # "PartyA":"254708374149",    
            # "PartyB":"174379",    
            # "PhoneNumber":"254708374149",    
            # "CallBackURL":"https://darajambili.herokuapp.com/express-payment",    
            # "AccountReference":"Test",    
            # "TransactionDesc":"Pay Hostel Booking Fee"

    }
    # simulate_response = requests.post(mpesa_endpoint,json=request_body,headers=headers)
    # return simulate_response.json()


    return 'Hello world'



def ac_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    data =(requests.get(mpesa_auth_url,auth = HTTPBasicAuth(consumer_key,consumer_secret)))
    data = data.json()
    return data['access_token']










    # simulate 
# @mpesa.route("/simulate")
# def simulate():
#     mpesa_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
#     access_token = ac_token()

#     headers = { "Authorization ":"Bearer %s" % ac_token()}

#     request_body = {

#         "ShortCode": "600992",
#         "CommandID": "CustomerPayBillOnline",
#         "BillRefNumber": "TestPay1",
#         "Msisdn": "254708374149",
#         "Amount":100
#     }
#     simulate_response = requests.post(mpesa_endpoint,json=request_body,headers=headers)
#     return simulate_response.json()

