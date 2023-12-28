import requests
import os
import json
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.environ.get("TOKEN")
APPLICATION_ID = os.environ.get("APPLICATION_ID")
URL = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

# Send the GET request
response = requests.get(URL, headers=headers).json()

with open('commands.json', 'w') as file:
    json.dump(response, file)

print(f"Downloaded JSON data saved to commands.json")