import os
import pandas as pd
import requests
import time
from twilio.rest import Client
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from credentials import Twilio_account_sid,Twilio_account_auth,Twilio_numer,weather_api
from utils import get_date,get_response,get_values_weather,to_dataFrame,get_plantilla_mensaje,send_message
import json

import tqdm as tqdm
from datetime import datetime


dia = get_date()

query = 'Lima'

response = get_response(query, weather_api)
datos =[]

for i in range(24):
    datos.append(get_values_weather(response, i))

nuevo_df = to_dataFrame(datos)

plantilla = get_plantilla_mensaje(dia, query,nuevo_df)

numero_receiver = '+51916017283'

enviar_mensaje = send_message(Twilio_account_sid, Twilio_account_auth, plantilla,Twilio_numer, numero_receiver)

print(f'Mensaje enviado {enviar_mensaje}')