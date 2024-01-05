import boto3


CONSTANTS = {
    'API_URL': "https://api.henrikdev.xyz"
}

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