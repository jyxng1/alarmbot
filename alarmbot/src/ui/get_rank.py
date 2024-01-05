import requests
from .utils import CONSTANTS, get_item_from_dynamodb


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

    response = requests.get(f"{CONSTANTS['API_URL']}/valorant/v2/mmr/na/{username}/{tag}")

    if response.status_code == 200:
        data = response.json()
        message_content = f"Current rank for {username}#{tag}: {data.get('data').get('current_data').get('currenttierpatched')} - {data.get('data').get('current_data').get('ranking_in_tier')} rr"
    else:
        message_content = f"Error from Valorant API: {response.status_code}"
    
    return message_content