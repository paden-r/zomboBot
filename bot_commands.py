import json
import random
import os
import discord
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv
from constants import (
    WEDNESDAY,
    IMAGES,
    IMAGE_FILE,
    VIDEO_FILE,
    USED_VIDEO_AND_IMAGES,
    VIDEO_INDEX,
    IMAGE_INDEX
)


class Zombot(commands.Bot):

    def __init__(self, **kwargs):
        default_commands = commands.DefaultHelpCommand(
            no_category="Common Commands"
        )

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=commands.when_mentioned_or('~'),
            description="A Bot for Zombocom",
            help_command=default_commands,
            case_insensitive=True,
            intents=intents,
            kwargs=kwargs
        )
        self.add_command(wednesday)
        self.add_command(dude)
        self.add_command(add_image)
        self.add_command(add_video)


@commands.command(name='dude', help='Responds with a random Wednesday video')
async def dude(ctx):
    videos = build_list(VIDEO_INDEX)
    response = random.choice(videos)
    mark_as_used(VIDEO_INDEX, response)
    await ctx.send(response)


@commands.command(name='wednesday', help='Responds with a Wednesday image')
async def wednesday(ctx):
    images = build_list(IMAGE_INDEX)
    response = random.choice(images)
    mark_as_used(IMAGE_INDEX, response)
    await ctx.send(response)


@commands.command(name='add_image', help='Adds image url to list of Wednesday images.  ~add_image [url to image]')
async def add_image(ctx, url=None):
    if url is not None:
        add_to_file(IMAGE_FILE, url)
        await ctx.send(f"added to the list")


@commands.command(name='add_video', help='Adds video url to list of Wednesday videos.  ~add_video [url to video]')
async def add_video(ctx, url=None):
    if url is not None:
        add_to_file(VIDEO_FILE, url)
        await ctx.send(f"added to the list")


def add_to_file(file_name, item):
    with open(file_name, 'w') as file_handle:
        file_handle.write(f"{item},")


def build_list(list_type: str):
    match list_type:
        case "images":
            list_to_use = IMAGES
            index = IMAGE_INDEX
            additional_file = IMAGE_FILE
        case "videos":
            list_to_use = WEDNESDAY
            index = VIDEO_INDEX
            additional_file = VIDEO_FILE
        case _:
            return []

    used_value = build_used_list(index)
    additional_values = None
    try:
        with open(additional_file, 'r') as file_handle:
            additional_values = file_handle.read()
    except FileNotFoundError:
        pass
    if additional_values:
        list_to_use.extend([x for x in additional_values.split(',') if x])

    trimmed_list = [x for x in list_to_use if x not in used_value]
    if not trimmed_list:
        clear_used_list(index)
        return build_list(list_type)
    return trimmed_list


def build_used_list(index=None):
    try:
        with open(USED_VIDEO_AND_IMAGES, 'r') as file_handle:
            used_dictionary = json.load(file_handle)
    except Exception as error:
        used_dictionary = {}
        print(f"No used file {error}")

    if not index:
        return used_dictionary
    return used_dictionary.get(index, [])


def mark_as_used(index, value):
    used_dictionary = build_used_list()
    used_list = used_dictionary.get(index)
    if not used_list:
        used_dictionary[index] = []
        used_list = used_dictionary[index]
    used_list.append(value)
    try:
        with open(USED_VIDEO_AND_IMAGES, 'w') as file_handle:
            json.dump(used_dictionary, file_handle)
    except Exception as error:
        print(f"Error writing used file: {error}")


def clear_used_list(index):
    used_dictionary = build_used_list()
    used_dictionary[index] = []
    try:
        with open(USED_VIDEO_AND_IMAGES, 'w') as file_handle:
            json.dump(used_dictionary, file_handle)
    except Exception as error:
        print(f"Error writing used file: {error}")


if __name__ == "__main__":
    dotenv_path = Path(".env_secret")
    load_dotenv(dotenv_path=dotenv_path)
    TOKEN = os.getenv("TOKEN")
    bot = Zombot()
    bot.run(TOKEN)
