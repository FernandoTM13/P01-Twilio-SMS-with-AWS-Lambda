import os
import pandas as pd
import requests
import time
from twilio.rest import Client
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from credentials import Twilio_account_sid,Twilio_account_auth,Twilio_numer,weather_api
import json

import tqdm as tqdm
from datetime import datetime


def get_date():
    date_now = datetime.now()
    date_now = date_now.strftime("%y-%m-%d")
    return date_now

def get_response(query,api_weather):
    url_weather = 'http://api.weatherapi.com/v1/forecast.json?key='+api_weather+'&q='+query+'&days=1&aqi=no&alerts=no'
    
    try:
        responseProd = requests.get(url_weather).json()
    except Exception as e:
        print(e)
    
    return responseProd

def get_values_weather(response, iterator):
    shortcut = response['forecast']['forecastday'][0]['hour']
    
    Day = shortcut[iterator]['time'].split()[0]
    Hour = int(shortcut[iterator]['time'].split()[1].split(':')[0])
    Condition=shortcut[iterator]['condition']['text']
    temperatura = shortcut[iterator]['temp_c']
    rain = shortcut[iterator]['will_it_rain']
    posibilidad = shortcut[iterator]['chance_of_rain']

    return Day, Hour, Condition, temperatura, rain, posibilidad


def to_dataFrame(lista):
    column = ['Day', 'Hour', 'Condition', 'temperatura', 'rain', 'posibilidad']
    df = pd.DataFrame(lista, columns=column)
    df = df[(df['posibilidad']>50) & (df['Hour']>6) & (df['Hour']<11)]
    df=df[['Hour','Condition','temperatura']]
    return df

def get_plantilla_mensaje(dia, ciudad, df):
    mensaje = f'''
    ---Prueba Amb. Desarrollo---
    Aquí tienes las noticias de temperatura para el día {dia} en la ciudad de {ciudad}:
    '''

    for index, row in df.iterrows():
        mensaje += f'''
        Hora: {row['Hour']}
        Condición: {row['Condition']}
        Temperatura: {row['temperatura']} 
        '''

    mensaje += '''
    ¡Saludos!
    '''
    
    return mensaje


def send_message(Twilio_account_sid,Twilio_account_auth,mensaje,Twilio_number,receive):
    account_sid = Twilio_account_sid
    auth_token = Twilio_account_auth
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
             body=mensaje,
             from_=Twilio_number,
             to=receive
         )

    return message.sid