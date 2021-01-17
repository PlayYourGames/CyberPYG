from typing import Union

import discord
from discord.ext import commands

from src.utils import *


class CyberPYG(commands.Bot):
    def __init__(self, prefix: str):
        """ Bot's constructor """

        super().__init__(command_prefix=prefix)
        self.bot_instance = self.user

    @commands.Cog.listener()
    async def on_ready(self):
        """ Bot's ready """

        print(f"Connecté en tant que {self.user}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Union[discord.User, discord.Member], before, after):
        """ Voice User State Update """

        if before.channel and after.channel:  # User's connected before and after the update
            print(1)
            if before.self_stream != after.self_stream:  # If user's currently streaming
                print(2)
                if "Salon de" in after.channel.name:  # If the channel's a private one
                    print(3)
                    print(member.status)


if __name__ == '__main__':
    bot_instance = CyberPYG(prefix='.')
    bot_token: str = retrieve_secret_data("TOKEN")

    bot_instance.run(bot_token)
