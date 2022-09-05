import requests
import random
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from constants import (
    DISCORD_URL,
    VIDEO_INDEX
)
from utilities import (
    build_list,
    mark_as_used
)

BIRTHDAY_GIF = "https://i.kym-cdn.com/photos/images/original/000/807/541/d8a.gif"


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
        video_list = build_list(VIDEO_INDEX)
        video_link = random.choice(video_list)
        mark_as_used(VIDEO_INDEX, video_link)
        message = f"It is Wednesday my dudes\n\n {video_link}"
        data = {
            "content": message
        }
        response = requests.post(f"{DISCORD_URL}/channels/{self.channel_id}/messages", headers=headers, data=data)
        print(response.json())

    def send_birthday(self, name):
        headers = {
            'Authorization': 'Bot ' + self.token
        }

        message = f"Happy Birthday {name}!!\n\n {BIRTHDAY_GIF}"
        data = {
            "content": message
        }
        response = requests.post(f"{DISCORD_URL}/channels/{self.channel_id}/messages", headers=headers, data=data)
        print(response.json())


if __name__ == "__main__":
    if not len(sys.argv) < 2:
        print("Missing arguments.")
    discord = Discord_Cron()
    command = sys.argv[1]
    match command:
        case "wednesday":
            discord.send_wednesday()
        case "birthday":
            try:
                name = sys.argv[2]
                discord.send_birthday(name)
            except IndexError:
                print("Missing name")
        case _:
            print(f"Unknown argument: {sys.argv[1]}")
