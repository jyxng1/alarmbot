import requests
import boto3

def default(data, member):
    URL = "https://api.henrikdev.xyz"

    username = data.get('options')[0].get('value')
    tag = data.get('options')[1].get('value')

    response = requests.get(f"{URL}/valorant/v1/account/{username}/{tag}")

    if response.status_code == 200:
        data = response.json()
        puuid = data.get('data').get('puuid')

        message_content = f"Default account has been changed to {username}#{tag}"

        dynamodb = boto3.resource('dynamodb')
        table_name = 'Alarmbot'
        table = dynamodb.Table(table_name)

        item = {
            'DiscordUserID': member.get('user').get('id'),
            'DiscordUsername': member.get('user').get('username'),
            'ValorantUsername': username,
            'ValorantTag': tag,
            'ValorantPUUID': puuid
        }
        response = table.put_item(Item=item)
    else:
        message_content = f"Error from Valorant API: {response.status_code}"

    return message_content

def get_rank(data):
    URL = "https://api.henrikdev.xyz"

    username = data.get('options')[0].get('value')
    tag = data.get('options')[1].get('value')

    response = requests.get(f"{URL}/valorant/v2/mmr/na/{username}/{tag}")

    if response.status_code == 200:
        data = response.json()
        message_content = f"Current rank for {username}#{tag}: {data.get('data').get('current_data').get('currenttierpatched')} - {data.get('data').get('current_data').get('ranking_in_tier')} rr"
    else:
        message_content = f"Error from Valorant API: {response.status_code}"
    
    return message_content
