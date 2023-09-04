import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import json
import random
import time
from datetime import datetime
import datetime
import os
import numpy as np 
from millify import millify,prettify
from tqdm import tqdm
#from cred_template import *
#import cred

API_KEY = 'xxXxxXXxxXXxxXXXXxxxxxXXXXXXxxxs'
DEVELOPER_KEY = API_KEY
#DEVELOPER_KEY = cred.API_KEY

url = "https://www.youtube.com/channel/UCLXRGxAzeaLDGaOphqapzmg"

CHANNEL_ID = 'UCLXRGxAzeaLDGaOphqapzmg'

url_channel_stats = 'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id='+CHANNEL_ID+'&key='+DEVELOPER_KEY
channel_stats = requests.get(url_channel_stats).json()

channel_stats = channel_stats['items'][0]['statistics']
date = pd.to_datetime('today').strftime("%Y-%m-%d")

data_channel = {
    
    'Created_at':date,
    'Total_Views':int(float(channel_stats['viewCount'])),
    'Suscribers':int(float(channel_stats['subscriberCount'])),
    'Video_count':int(float(channel_stats['videoCount'])),
    
}

def get_stats(api_key,channel_id):
    
    url_channel_stats = 'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id='+channel_id+'&key='+api_key
    channel_stats = requests.get(url_channel_stats).json()
    
    
    channel_stats = channel_stats['items'][0]['statistics']
    date = pd.to_datetime('today').strftime("%Y-%m-%d")

    data_channel = {

        'Created_at':date,
        'Total_Views':int(float(channel_stats['viewCount'])),
        'Suscribers':int(float(channel_stats['subscriberCount'])),
        'Video_count':int(float(channel_stats['videoCount'])),

    }
    
    return data_channel

channels_name  =  ['DeigoRuzzarin', 'NateGentile','Marciaylanube','Fazt_web','PeladoNerd','Codigofacilito']
channels_id  =  ['UC1viRct91s1a3Z5yvk7FJXw', 'UC36xmz34q02JYaZYKrMwXng','UCWYUbW_Lw5EQC0WybxInObA','UCoMdktPbSTixAyNGwb-UYkQ','UCrBzBOMcUVV8ryyAU_c6P5g','UCLXRGxAzeaLDGaOphqapzmg']

channels = {
    'Channel_name':channels_name,
    'Channel_id':channels_id}

df_channels = pd.DataFrame(channels)

# Exportar el DataFrame a un archivo CSV
df_channels.to_csv('channels_to_analize.csv', index=False)
