import logging
import json
import discord
import traceback
from typing import Union, Dict, Any

from discord import Invite
from discord.ext import commands
config: dict


client = discord.Client(intents=discord.Intents().all())
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

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_error(event, *args, **kwargs):
    channelException = client.get_channel(config["channels"]["error_channel"])
    logging.warning(traceback.format_exc()) #logs the error
    await channelException.send("** Exception depuis %s: **\n```%s```" % (event, traceback.format_exc()))

def getChannelName(member, game):
    return f"{game.name} - {member.name}"
async def onMemberJoinChannel(member, before, after):
    if member is not None and before.channel is not None: # Leaving streaming channel
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

    if after.channel is not None and after.channel.id == config["channels"]["voice_channel"]: # Joining streaming channel
        game = getMemberGame(member)
        guild = member.guild
        new_voice_channel = None
        new_text_channel = None
        if game is not None: # If a game is detected
            new_voice_channel = await guild.create_voice_channel(name=getChannelName(member, game), category=after.channel.category)
            new_text_channel = await guild.create_text_channel(name=getChannelName(member, game), category=after.channel.category)
        else: # TODO : Create personal room if player is not playing
            new_voice_channel = await guild.create_voice_channel(name=f"Salon de {member.display_name}", category=after.channel.category)
            new_text_channel = await guild.create_text_channel(name=f"Salon de {member.display_name}", category=after.channel.category)
        print(f"[CHANNEL] Creating voice channel '{new_voice_channel.name} and text channel '{new_text_channel.name}")
        ChannelType.streamingChannels[new_voice_channel.id] = ChannelType(new_voice_channel, new_text_channel)
        ChannelType.streamingChannels[new_voice_channel.id].streamerId = member.id
        ChannelType.streamingChannels[new_voice_channel.id].game = game
        await member.move_to(new_voice_channel)
@client.event
async def on_voice_state_update(member: discord.Member, before, after):

    """ Voice User State Update """
    #old_name: str = after.channel.name
    #print(f"Old name = {old_name}")
    if before.channel != after.channel: # Triggered when a member joins or leaves a channel
        await onMemberJoinChannel(member, before, after)
    if not before.self_stream and after.self_stream:  # Triggering start stream event
        await onSelfStreamStart(member, after.channel)
    elif before.self_stream and not after.self_stream: # Triggering end stream event
        await onSelfStreamEnd(member, before.channel)


async def onSelfStreamStart(member, channel): # Triggered when self stream starting
    if channel is not None and channel.id in ChannelType.streamingChannels:
        game = getMemberGame(member)
        if member.id == ChannelType.streamingChannels[channel.id].streamerId and getMemberGame(member) != None:
            default_channel = member.guild.get_channel(config["channels"]["text_channel"])
            channel_name = getChannelName(member, game)
            if channel.name != channel_name and ChannelType.streamingChannels[channel.id].editTimes < 2:
                await channel.edit(name=channel_name)
                await ChannelType.streamingChannels[channel.id].channelText.edit(name=channel_name)
                ChannelType.streamingChannels[channel.id].editTimes = ChannelType.streamingChannels[channel.id].editTimes + 1
            print(f"[STREAM] Streaming {game.name} from {member.display_name}")
            invitation:Invite = await channel.create_invite(reason=f'{member.mention} a débuté son stream sur {game.name}')
            await default_channel.send(f'{member.mention} a débuté son stream sur **{game.name}**\nRejoignez le dès maintenant !\n|| {invitation.url} ||')


async def onSelfStreamEnd(member, channel:discord.VoiceChannel): # Triggered when self stream ending
    pass
def getMemberGame(member): # Get the game a user is playing
    game_activity = None
    """ Check throughout the different activities the user may have """
    for i in range(len(member.activities)):
        if member.activities[i].type.__eq__(discord.ActivityType.playing):
            game_activity = member.activities[i]
    return game_activity

def main():
    with open('config.json', "r") as configFile:
        data: Dict = json.loads(configFile.read())
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
