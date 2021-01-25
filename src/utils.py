import json
import os

import discord


class ChannelType:
    channelVoice = None
    streamerId = -1
    streamingChannels = {}
    channelText = None
    game = None
    editTimes = 0
    def __init__(self, channelVoice:discord.VoiceChannel, channelText:discord.TextChannel):
        self.channelVoice = channelVoice
        self.channelText = channelText
        #ChannelType.streamingChannels[channelId] = self

async def send_dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)

def retrieve_secret_data(key: str):
    """ Retrieve data from a key string """

    with open('config/env.json', 'r+') as file:
        data = json.load(file)
    return data[key]


def load_cogs(_client, subdir: str) -> None:
    """ Load subfolder cogs """

    for _cog in [file.split(".")[0] for file in os.listdir(f'cogs/{subdir}') if file.endswith('.py')]:
        subdir = subdir.replace('/', '.')
        try:
            _client.load_extension(f'cogs.{subdir}.{_cog}') if _cog != '__init__' else ...
        except Exception as e:
            print(e)


async def safe_delete(ctx) -> None:
    """ Deleting user command message bypassing permission error """

    try:
        await ctx.message.delete()
    except Exception as _:
        pass
