from typing import Union

import discord
from discord.ext import commands


class Stream_VC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Union[discord.User, discord.Member], before, after):
        """ Voice User State Update """

        if before.channel and after.channel:  # User's connected before and after the update
            if before.self_stream != after.self_stream:  # If user's currently streaming
                if "Salon de" in after.channel.name:  # If the channel's a private one
                    print(member.status)  # Status is limited.
                    # :todo: Retrieving from Discord API user's streaming presence


def setup(bot):
    bot.add_cog(Stream_VC(bot))
