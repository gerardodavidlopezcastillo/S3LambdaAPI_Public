import json
import pandas as pd
import time
import requests
import random
import time
import boto3
from datetime import datetime
import datetime
import os

s3_client = boto3.client('s3')

def get_stats(api_key,channel_id):
    
    url_channel_stats = 'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id='+channel_id+'&key='+api_key
    response_channels = requests.get(url_channel_stats)
    channel_stats = json.loads(response_channels.content)
    channel_stats = channel_stats['items'][0]['statistics']
    date = pd.to_datetime('today').strftime("%Y-%m-%d")

    data_channel = {

            'Date':date,
            'Total_Views':int(float(channel_stats['viewCount'])),
            'Subscribers':int(float(channel_stats['subscriberCount'])),
            'Video_count':int(float(channel_stats['videoCount']))
                        }

    return data_channel

def channels_stats(df,api_key):
    
    date = []
    views = []
    suscriber = []
    video_count = []
    channel_name = []
    
    tiempo = [1,2.5,2]
    
    for i in range(len(df)):
        
        stats_temp = get_stats(api_key,df['Channel_id'][i])
        
        channel_name.append(df['Channel_name'][i])
        date.append(stats_temp['Date'])
        views.append(stats_temp['Total_Views'])
        suscriber.append(stats_temp['Subscribers'])
        video_count.append(stats_temp['Video_count'])
     
    time.sleep(random.choice(tiempo))
    
    data = {
        
        'Channel_name':channel_name,
        'Subscribers':suscriber,
        'Video_count':video_count,
        'Total_Views':views,
        'Createt_at':date,
    }
    
    df_channels = pd.DataFrame(data)
    
    return df_channels

def lambda_handler(event, context):
    
    bucket_name = os.environ['BUCKET_RAW']
    filename =  os.environ['FILE_CHANNELS']
    DEVELOPER_KEY = os.environ['APIKEY']
    
    # Get File from S3
    obj = s3_client.get_object(Bucket=bucket_name, Key= filename)
    df_channels = pd.read_csv(obj['Body']) # 'Body' is a key word
    
    results = channels_stats(df_channels,DEVELOPER_KEY)
    date = pd.to_datetime('today').strftime("%Y%m%d")
    
    results.to_csv(f'/tmp/youtube_stats_{date}.csv',index = False)
 
    # Send file to  S3
    s3 = boto3.resource("s3")
    
    s3.Bucket(os.environ['BUCKET_STAGE']).upload_file(f'/tmp/youtube_stats_{date}.csv', Key=f'youtube_stats_{date}.csv')
    os.remove(f'/tmp/youtube_stats_{date}.csv')

    return f'file youtube_stats_{date}.csv send succeded'
