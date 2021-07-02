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
from requests.auth import HTTPBasicAuth
import unicodedata, re, itertools, sys


mpesa = Blueprint("mpesa", __name__, url_prefix="/mpesa")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# *** Authorization Request in Python ***|

# mpesa details

consumer_key = 'rKCtIJJqQF8fU3Chw508Bl5JMCwIh5xn'
consumer_secret = 'Bi4gdEUCOmPpmkcx'
base_url = 'http://102.167.16.174'

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

# simulate 
@mpesa.route("/simulate")
def simulate():
    mpesa_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    access_token = ac_token()

    headers = { "Authorization ":"Bearer %s" % ac_token()}

    request_body = {

        "ShortCode": "600992",
        "CommandID": "CustomerPayBillOnline",
        "BillRefNumber": "TestPay1",
        "Msisdn": "254708374149",
        "Amount":100
    }
    simulate_response = requests.post(mpesa_endpoint,json=request_body,headers=headers)
    return simulate_response.json()



def ac_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    data =(requests.get(mpesa_auth_url,auth = HTTPBasicAuth(consumer_key,consumer_secret)))
    data = data.json()
    return data['access_token']