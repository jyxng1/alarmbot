import requests
import boto3
from .utils import CONSTANTS


def default(data, member):
    username = data.get('options')[0].get('value')
    tag = data.get('options')[1].get('value')

    response = requests.get(f"{CONSTANTS['API_URL']}/valorant/v1/account/{username}/{tag}")

    if response.status_code == 200:
        data = response.json()
        puuid = data.get('data').get('puuid')

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Alarmbot')

        item = {
            'DiscordUserID': member.get('user').get('id'),
            'DiscordUsername': member.get('user').get('username'),
            'ValorantUsername': username,
            'ValorantTag': tag,
            'ValorantPUUID': puuid
        }
        response = table.put_item(Item=item)

        message_content = f"Default account has been changed to {username}#{tag}"
    else:
        message_content = f"Error from Valorant API: {response.status_code}"

    return message_content
