import random
import logging
import os
from pathlib import Path

import discord
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from constants import WEDNESDAY

# In case to disable logging
logging.getLogger("apscheduler.executors.default").propagate = False

class Discord_Bot:
    def __init__(self):
        dotenv_path = Path(".env_secret")
        load_dotenv(dotenv_path=dotenv_path)
        self.client = discord.Client()
        self.TOKEN = os.getenv("TOKEN")
        self.channel_id = int(os.getenv("CHANNEL_ALPY"))
        try:
            self.client.loop.create_task(self.task())
            self.client.loop.run_until_complete(self.client.start(self.TOKEN))
        except SystemExit:
            pass
            # handle_exit()
        except KeyboardInterrupt:
            # handle_exit()
            self.client.loop.close()
            print("Program ended.")

    async def task(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.wednesday, "cron", day="3", hour="8")
        scheduler.start()

    async def send_message(self, msg=""):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(self.channel_id)
        if not msg:
            msg = f"Tick! The time is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        await channel.send(msg)

    async def wednesday(self):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(self.channel_id)
        video_link = random.choice(WEDNESDAY)
        await channel.send(video_link)


_discord = Discord_Bot()