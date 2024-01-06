import requests
from .utils import CONSTANTS, get_user_info


def get_rank(data, member):
    username, tag = get_user_info(data.get('options'), member)

    response = requests.get(f"{CONSTANTS['API_URL']}/valorant/v2/mmr/na/{username}/{tag}")

    if response.status_code == 200:
        data = response.json()
        message_content = f"Current rank for {username}#{tag}: {data.get('data').get('current_data').get('currenttierpatched')} - {data.get('data').get('current_data').get('ranking_in_tier')} rr"
    else:
        message_content = f"Error from Valorant API: {response.status_code}"
    
    return message_content