import discord
from discord.ext import commands

from utils import *


class CyberPYG(commands.Bot):
    def __init__(self, prefix: str):
        """ Bot's constructor """

        super().__init__(command_prefix=prefix, intents=discord.Intents().all())
        self.bot_instance = self.user

    @commands.Cog.listener()
    async def on_ready(self):
        """ Bot's ready """

        load_cogs(self, subdir='stats')
        print(f"Connecté en tant que {self.user}")


if __name__ == '__main__':
    bot_instance = CyberPYG(prefix='.')
    bot_token: str = retrieve_secret_data("TOKEN")

    bot_instance.run(bot_token)
