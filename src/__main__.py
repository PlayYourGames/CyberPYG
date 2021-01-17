from discord.ext import commands

from src.utils import *


class CyberPYG(commands.Bot):
    def __init__(self, prefix: str):
        super().__init__(command_prefix=prefix)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Connecté en tant que {self.user}")


if __name__ == '__main__':
    bot_instance = CyberPYG(prefix='.')
    bot_token: str = retrieve_secret_data("TOKEN")

    bot_instance.run(bot_token)
