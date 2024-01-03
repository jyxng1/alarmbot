import requests
import boto3
from datetime import datetime
from .data import API_URL


def get_item_from_dynamodb(primary_key_value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Alarmbot')
    key_value = {'DiscordUserID': primary_key_value}

    try:
        response = table.get_item(Key=key_value)
        if 'Item' in response:
            item = response['Item']
        else:
            return None
    except Exception as e:
        return None
    
    return item

def help():
    message_content = """
    **Alarmbot commands**
    `/default` - Set default Valorant account
    `/rank` - Get rank and rr for an account
    `/recent` - Display stats from most recent game for selected gamemode
    `/overall` - Display aggregate stats [WIP]
    `/history` - Show log of recent matches played, with IDs [WIP]
    `/match` - Retrieve details about a specific match from its ID [WIP]
    """
    return message_content

def default(data, member):
    username = data.get('options')[0].get('value')
    tag = data.get('options')[1].get('value')

    response = requests.get(f"{API_URL}/valorant/v1/account/{username}/{tag}")

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

def get_rank(data, member):
    if data.get('options') is None:
        item = get_item_from_dynamodb(member.get('user').get('id'))
        if item:
            username = item.get('ValorantUsername')
            tag = item.get('ValorantTag')
        else:
            message_content = "Please set a default account first or specify a username and tag"
            return message_content
    else:
        username = data.get('options')[0].get('value')
        tag = data.get('options')[1].get('value')

    response = requests.get(f"{API_URL}/valorant/v2/mmr/na/{username}/{tag}")

    if response.status_code == 200:
        data = response.json()
        message_content = f"Current rank for {username}#{tag}: {data.get('data').get('current_data').get('currenttierpatched')} - {data.get('data').get('current_data').get('ranking_in_tier')} rr"
    else:
        message_content = f"Error from Valorant API: {response.status_code}"
    
    return message_content

def retrieve_stats(data):
    map = data.get('meta').get('map').get('name')
    mode = data.get('meta').get('mode')
    time = datetime.strptime(data.get('started_at'), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y %H:%M:%S")
    team = data.get('stats').get('team').lower()
    agent = data.get('stats').get('character').get('name')

def get_recent_summary(data, member):
    options = data.get('options').get('options')

    if options is None and options[0].get('name') is not "username" and options[1].get('name') is not "tag":
        item = get_item_from_dynamodb(member.get('user').get('id'))
        if item:
            username = item.get('ValorantUsername')
            tag = item.get('ValorantTag')
        else:
            message_content = "Please set a default account first or specify a username and tag"
            return message_content
    else:
        username = options[0].get('value')
        tag = data.get('options').get('options')[1].get('value')

    extras = "?size=1"
    for option in options:
        if option.get("name") == "map":
            extras += "&map=" + option.get("value")
        if option.get("name") == "mode":
            extras += "&mode=" + option.get("value")

    response = requests.get(f"{API_URL}/valorant/v1/lifetime/matches/na/{username}/{tag}{extras}")

    if response.status_code == 200:
        data = response.json()
        message_content = retrieve_stats(data.get('data')[0])
    else:
        message_content = f"Error from Valorant API: {response.status_code}"
    
    return message_content

def get_recent_full(data, member):
    return "Not implemented yet"