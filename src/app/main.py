import json
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dotenv import load_dotenv

from val_api import get_rank, default


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
    command_name = data["name"]

    if command_name == "default":
        message_content = default(data, raw_request["member"])
    elif command_name == "rank":
        message_content = get_rank(data)
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
        message_content = process_request(raw_request)

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }
    
    print(response_data)
    return json.dumps(response_data)
