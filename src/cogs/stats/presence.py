from typing import Union

import discord
from attr import dataclass
from discord.ext import commands

from src.utils import safe_delete


@dataclass
class ActivityChannel:
    channel: discord.TextChannel
    author: Union[discord.Member, discord.User]
    message_amount: int


class StatisticsPresence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activity_channels: dict = {}
        self.user_activity: dict = {}

    @commands.command(name='activty')
    async def activity(self, ctx):
        await safe_delete(ctx)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """ When a message is found by the API """

        if message.author is not message.author.bot:  # If the message's not comming from a bot
            self.increment_user_amount(message.author)
            print(f"{self.user_activity}")

    def increment_user_amount(self, target: Union[discord.Member, discord.User]):
        """ User message amount handler"""

        if target not in self.user_activity:
            self.user_activity[target] = 1
        else:
            self.user_activity[target] += 1


def setup(bot):
    bot.add_cog(StatisticsPresence(bot))
