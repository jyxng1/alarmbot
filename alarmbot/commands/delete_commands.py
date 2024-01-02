import requests
import os
import json
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.environ.get("TOKEN")
APPLICATION_ID = os.environ.get("APPLICATION_ID")
COMMAND_ID = 1190039154378154035
URL = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands/{COMMAND_ID}"

headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

# Send the GET request
response = requests.delete(URL, headers=headers)