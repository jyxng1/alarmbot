import datetime
import requests
from .utils import CONSTANTS, get_item_from_dynamodb


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

    response = requests.get(f"{CONSTANTS['API_URL']}/valorant/v1/lifetime/matches/na/{username}/{tag}{extras}")

    if response.status_code == 200:
        data = response.json()
        message_content = retrieve_stats(data.get('data')[0])
    else:
        message_content = f"Error from Valorant API: {response.status_code}"
    
    return message_content