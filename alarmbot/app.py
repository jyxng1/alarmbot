
# TODO: JUST LET THE HANDLER FUNCTION
#       IF SOMETHING IS NEEDED, IMPORT FROM SRC
#       THIS IS A MESS

# import src
# something = src.something()

import json
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dotenv import load_dotenv

from val_api import help, default, get_rank, get_recent_summary, get_recent_full


load_dotenv()

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")

def verify_signature(event, raw_body):
    auth_sig = event['headers'].get('x-signature-ed25519')
    auth_ts  = event['headers'].get('x-signature-timestamp')
    
    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig))

def process_request(raw_request):
    data = raw_request["data"]
    member = raw_request["member"]
    command_name = data["name"]

    if command_name == "default":
        message_content = default(data, member)
    elif command_name == "rank":
        message_content = get_rank(data, member)
    elif command_name == "help":
        message_content = help()
    elif command_name == "recent":
        if data.get('options').get('name') == 'summary':
            message_content = get_recent_summary(data, member)
        else:
            message_content = get_recent_full(data, member)
    return message_content

def handler(event, context):
    raw_request = event["body"]
    print(raw_request)

    try:
        verify_signature(event, raw_request)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    raw_request = json.loads(raw_request)

    if raw_request["type"] == 1:  # PING
        response_data = {"type": 1}  # PONG
    else:
        try:
            message_content = process_request(raw_request)
        except Exception as e:
            message_content = f"Request error: {e}"

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }
    
    print(response_data)
    return json.dumps(response_data)
