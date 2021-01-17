from discord.ext import commands

from src.utils import safe_delete


class StatisticsPresence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='activty')
    async def activity(self, ctx):
        await safe_delete(ctx)
