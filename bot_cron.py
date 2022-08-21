import requests
import random
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from constants import WEDNESDAY, DISCORD_URL


class Discord_Cron:
    def __init__(self):
        dotenv_path = Path(".env_secret")
        load_dotenv(dotenv_path=dotenv_path)
        self.token = os.getenv("TOKEN")
        self.channel_id = int(os.getenv("CHANNEL_ALPY"))

    def send_wednesday(self):
        headers = {
            'Authorization': 'Bot ' + self.token
        }
        video_link = random.choice(WEDNESDAY)
        message = f"It is Wednesday my dudes\n\n {video_link}"
        data = {
            "content": message
        }
        response = requests.post(f"{DISCORD_URL}/channels/{self.channel_id}/messages", headers=headers, data=data)
        print(response.json())


if __name__ == "__main__":
    discord = Discord_Cron()
    if not len(sys.argv) == 2:
        print("Missing arguments.")
    elif sys.argv[1] in ['wednesday']:
        if sys.argv[1] == 'wednesday':
            discord.send_wednesday()
    else:
        print(f"Unknown argument: {sys.argv[1]}")
