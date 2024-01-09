import json
import os
import traceback
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dotenv import load_dotenv

from ..ui import help, default, get_rank, get_recent_summary, get_recent_full


def verify_signature(event, raw_body):
    load_dotenv()
    PUBLIC_KEY = os.environ.get("PUBLIC_KEY")

    auth_sig = event['headers'].get('x-signature-ed25519')
    auth_ts  = event['headers'].get('x-signature-timestamp')
    
    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig))

def maintenance_switch(member):
    load_dotenv()
    maintenance_mode = os.environ.get("MAINTENANCE_MODE")
    allowlist = os.environ.get("USER_MAINTENANCE_ALLOW_LIST").split()
    return maintenance_mode != "ON" or member["user"]["id"] in allowlist

def send_command(raw_request):
    data = raw_request["data"]
    member = raw_request["member"]
    command_name = data["name"]

    if maintenance_switch(member):
        message_content = "Bot is currently under maintenance. Please try again later."
        return message_content

    if command_name == "default":
        message_content = default(data, member)
    elif command_name == "rank":
        message_content = get_rank(data, member)
    elif command_name == "help":
        message_content = help()
    elif command_name == "recent":
        if data.get('options')[0].get('name') == 'summary':
            message_content = get_recent_summary(data, member)
        else:
            message_content = get_recent_full(data, member)
    return message_content

def run(event):
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
            message_content = send_command(raw_request)
        except Exception:
            message_content = f"Request error: {traceback.format_exc()}"

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }
    
    print(response_data)
    return json.dumps(response_data)