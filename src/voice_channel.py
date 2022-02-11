import logging
import json
from datetime import datetime

import discord
import traceback
import discord_components
import requests

from typing import Union, Dict, Any

from discord import Invite
from discord.ext import commands
import random

DEV = False

config:dict=None

client = discord.Client(intents=discord.Intents().all())


class ChannelType:
    channelVoice = None
    streamerId = -1
    streamingChannels = {}
    channelText = None
    game = None
    editTimes = 0

    def __init__(self, channelVoice: discord.VoiceChannel, channelText: discord.TextChannel):
        self.channelVoice = channelVoice
        self.channelText = channelText
        # ChannelType.streamingChannels[channelId] = self


@client.event
async def on_ready():
    global DEV
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    if DEV:
        print("Running in Development Environment")
    else:
        print("Running in Production Environment")
    print('------')


def requestIGDB(method: str, endpoint: str, data):
    access_token = connectToIGDB(config["igdb"]["client_id"], config["igdb"]["client_secret"])
    if method == "POST":
        req = requests.post(f"https://api.igdb.com/v4/{endpoint}", data,
                            headers={"Authorization": f"Bearer {access_token}",
                                     "Client-ID": config["igdb"]["client_id"]})
    response = req.json()
    if response is None or len(response) == 0:
        return None
    return req.json()[0]


def connectToIGDB(client_id: str, client_secret: str):
    print("Connecting to IGDB ...")
    request = requests.post(
        f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials")
    return request.json()["access_token"]


@client.event
async def on_error(event, *args, **kwargs):
    channelException = client.get_channel(config["channels"]["error_channel"])
    logging.warning(traceback.format_exc())  # logs the error
    await channelException.send("** Exception depuis %s: **\n```%s```" % (event, traceback.format_exc()))


def getVoiceChannelName(member, game):
    # Formats voice channel names depending on the member and the game played
    if game is not None:
        return f"🔊・{game.name} - {member.name}"
    return f"🔊・Salon de {member.display_name}"


def getTextChannelName(member, game):
    # Formats text channel names depending on the member and the game played
    if game is not None:
        return f"💬・{game.name} - {member.name}"
    return f"💬・Salon de {member.display_name}"


async def onMemberJoinChannel(member, before, after):
    if member is not None and before.channel is not None:  # Leaving streaming channel
        channel = before.channel
        channelType = ChannelType.streamingChannels.get(channel.id) if before is not None else None
        if channelType is not None and len(channel.members) <= 0:
            text_channel = ChannelType.streamingChannels[channel.id].channelText
            try:
                await channel.delete()
                await text_channel.delete()
                del ChannelType.streamingChannels[channel.id]
            except (KeyError, discord.errors.NotFound):
                pass

    if after.channel is not None and after.channel.id == config["channels"][
        "voice_channel"]:  # Joining streaming channel
        game = getMemberGame(member)
        guild = member.guild
        new_voice_channel = await guild.create_voice_channel(name=getVoiceChannelName(member, game),
                                                             category=after.channel.category)
        overwrite:discord.PermissionOverwrite = discord.PermissionOverwrite()
        overwrite.manage_channels = True
        await new_voice_channel.set_permissions(member, overwrite=overwrite)
        new_text_channel = await guild.create_text_channel(name=getTextChannelName(member, game),
                                                           category=after.channel.category)
        await new_text_channel.set_permissions(member, overwrite=overwrite)
        ChannelType.streamingChannels[new_voice_channel.id] = ChannelType(new_voice_channel, new_text_channel)
        ChannelType.streamingChannels[new_voice_channel.id].streamerId = member.id
        ChannelType.streamingChannels[new_voice_channel.id].game = game
        await member.move_to(new_voice_channel)


@client.event
async def on_voice_state_update(member: discord.Member, before, after):
    """ Voice User State Update """
    if before.channel != after.channel:  # Triggered when a member joins or leaves a channel
        await onMemberJoinChannel(member, before, after)
    if not before.self_stream and after.self_stream:  # Triggering start stream event
        await onSelfStreamStart(member, after.channel)
    elif before.self_stream and not after.self_stream:  # Triggering end stream event
        await onSelfStreamEnd(member, before.channel)


async def onSelfStreamStart(member, channel):  # Triggered when self stream starting
    if channel is not None and channel.id in ChannelType.streamingChannels:
        game = getMemberGame(member)
        if getMemberGame(member) != None:
            channel_name = getVoiceChannelName(member, game)
            if member.id == ChannelType.streamingChannels[channel.id].streamerId and channel.name != channel_name and ChannelType.streamingChannels[channel.id].editTimes < 2:
                await channel.edit(name=channel_name)
                await ChannelType.streamingChannels[channel.id].channelText.edit(name=getTextChannelName(member, game))
                ChannelType.streamingChannels[channel.id].editTimes = ChannelType.streamingChannels[
                                                                          channel.id].editTimes + 1

            await sendAnnounce(member, game, channel)


async def sendAnnounce(member, game, channel):
    """ Sends an announce when a member is streaming a game from the specified channel"""
    invitation: Invite = await channel.create_invite()

    embed = discord.Embed(title=f"🔊・{game.name} - {member.display_name}", url=invitation.url,
                          description=f"**{member.mention}** vient de lancer un stream sur **{game.name}**. N'hésitez pas à le rejoindre !",
                          color=0x25e000)
    response = requestIGDB("POST", "games", f"fields *; where name=\"{game.name}\";")
    if response is not None and "screenshots" in response:
        screenshot = random.choice(response["screenshots"])  # Takes randomly a screenshot from the retrieved list
        response = requestIGDB("POST", "screenshots", f"fields url; where id={screenshot};")
        url: str = response["url"]
        if url is not None:
            url = url.replace("//", "https://")
        embed.set_thumbnail(url=url)
    embed.set_footer(text=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
    default_channel = member.guild.get_channel(config["channels"]["text_channel"])
    await default_channel.send(embed=embed, components=[
        discord_components.Button(style=discord_components.ButtonStyle.URL, label="🔉・Rejoindre le vocal",
                                  url=invitation.url)])


async def onSelfStreamEnd(member, channel: discord.VoiceChannel):  # Triggered when self stream ending
    pass


def getMemberGame(member):  # Get the game a user is playing
    game_activity = None
    """ Check throughout the different activities the user may have """
    for i in range(len(member.activities)):
        if member.activities[i].type.__eq__(discord.ActivityType.playing):
            game_activity = member.activities[i]
    return game_activity


def main():
    global DEV
    with open('config.json', "r") as configFile:
        raw: Dict = json.loads(configFile.read())
        if DEV:
            data = raw["dev"]
        else:
            data = raw["prod"]
    if data is None:
        print("[ERROR] Unable to read from config.json file")
    else:
        if "bot_token" in data:
            global config
            config = data
            client.run(config["bot_token"])
        else:
            print("[ERROR] Unable to parse bot_token value")


if __name__ == "__main__":
    main()

print(__name__)
