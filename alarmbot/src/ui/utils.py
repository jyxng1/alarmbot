import boto3


CONSTANTS = {
    'API_URL': "https://api.henrikdev.xyz",
    'ERROR_MESSAGE': "An error occurred. Please try again later."
}

def get_item_from_dynamodb(primary_key_value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Alarmbot')
    key_value = {'DiscordUserID': primary_key_value}

    response = table.get_item(Key=key_value)
    if 'Item' in response:
        return response['Item']
    else:
        return None
    
def get_user_info(options, member):
    if options is None or not options or (options and options[0].get('name') != "username" and options[1].get('name') != "tag"):
        item = get_item_from_dynamodb(member.get('user').get('id'))
        if item:
            username = item.get('ValorantUsername')
            tag = item.get('ValorantTag')
        else:
            message_content = "Please set a default account first or specify a username and tag"
            return message_content
    else:
        username = options[0].get('value')
        tag = options.get('options')[1].get('value')
    return username, tag