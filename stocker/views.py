# importar la biblioteca de registro
import logging


from datetime import datetime, timedelta

import requests
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token

from stocker.models import Customer


# Obtener una instancia de un registrador
logger = logging.getLogger(__name__)


@api_view(["POST"])
@parser_classes([JSONParser])
def create_user(request):

    customer_name = request.data.get("name", None)
    customer_last_name = request.data.get("last", None)
    customer_mail = request.data.get("mail", None)
    customer_username = request.data.get("username", None)
    customer_password = request.data.get("password", None)
    logger.info("Signing up")
    to_check_list = [
        customer_name,
        customer_last_name,
        customer_mail,
        customer_username,
        customer_password,
    ]

    if any([info is None for info in to_check_list]):
        logger.warning("Signing up Failed")
        return Response(
            "Some sign-up parameters not added in request", status=HTTP_400_BAD_REQUEST
        )

    try:
        validate_email(customer_mail)
        Customer.objects.create_user(
            customer_username,
            customer_mail,
            customer_password,
        )
    except IntegrityError:
        logger.warning("Signing up Failed")
        return Response("Username or mail already exist", status=HTTP_400_BAD_REQUEST)
    except ValidationError:
        logger.warning("Signing up Failed")
        return Response("Invalid mail format", status=HTTP_400_BAD_REQUEST)

    return Response("User Created", status=HTTP_200_OK)


@api_view(["GET"])
@parser_classes([JSONParser])
def login_user(request):

    customer_username = request.data.get("username", None)
    customer_password = request.data.get("password", None)

    logger.info("Logging in")
    to_check_list = [
        customer_username,
        customer_password,
    ]

    if any([info is None for info in to_check_list]):
        return Response(
            "Some login parameters not added in request", status=HTTP_400_BAD_REQUEST
        )

    customer = authenticate(username=customer_username, password=customer_password)

    if customer is None:
        logger.warning("Logging in Failed")
        return Response(
            "User Name or password doesn't exist", status=HTTP_404_NOT_FOUND
        )

    token, created = Token.objects.get_or_create(user=customer)

    return Response({"Authorization": token.key}, status=HTTP_200_OK)


@api_view(["GET"])
@parser_classes([JSONParser])
def get_ticker_prices(request):
    token_key = request.META.get("HTTP_AUTHORIZATION")

    ticker = request.data.get("ticker", None)
    token = Token.objects.get(key=token_key)
    logger.info(f"Ticker received {ticker}")
    if token is None:
        return Response("Token Invalido", status=HTTP_400_BAD_REQUEST)

    if ticker is None:
        return Response("No Ticker Assigned", status=HTTP_400_BAD_REQUEST)

    url = "https://www.alphavantage.co"
    endpoint = "/query"

    payload = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "compact",
        "apikey": "X86NOH6II01P7R24",
    }
    r = requests.get(url + endpoint, params=payload)
    data = r.json()
    last_date_str = data["Meta Data"]["3. Last Refreshed"]
    logger.info(f"Last Refreshed Date {last_date_str}")
    last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
    last_last_date = (last_date - timedelta(days=1)).strftime("%Y-%m-%d")
    data["Time Series (Daily)"][last_last_date]["4. close"]
    result = data["Time Series (Daily)"][last_date_str]
    result.update(
        {
            "close deviation": "{:.4f}".format(
                float(data["Time Series (Daily)"][last_date_str]["4. close"])
                - float(data["Time Series (Daily)"][last_last_date]["4. close"])
            )
        }
    )

    return Response(data=result, status=HTTP_200_OK)
