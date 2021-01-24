from typing import Union

import discord
from discord.ext import commands


class Stream_VC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        """ Voice User State Update """

        if before.channel and after.channel:  # User's connected before and after the update
            if before.self_stream != after.self_stream:  # If user's currently streaming
                if "Salon de" in after.channel.name:  # If the channel's a private one
                    user_channel = member.voice.channel
                    game_activity = None

                    """ Check throughout the different activities the user may have """
                    for i in range(len(member.activities)):
                        if member.activities[i].type.__eq__(discord.ActivityType.playing):
                            game_activity = member.activities[i]

                    await user_channel.edit(name=f"{game_activity.name} - {member.name}")


def setup(bot):
    bot.add_cog(Stream_VC(bot))
