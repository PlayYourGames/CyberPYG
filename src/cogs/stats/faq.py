from discord import Embed
from discord.ext import commands
from utils import safe_delete, load_faq

import pprint


class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='spawn_faq')
    async def activity(self, ctx):
        await safe_delete(ctx)
        data: list = load_faq()

        blank_embed = Embed(
            description="Et si vous portiez un peu d'attention aux questions les plus posées sur P-Y-G ?",
            color=0x2F3136)

        for iterator in range(len(data)):
            blank_embed.add_field(name=f"**{data[str(iterator)]['question']}**", value=data[str(iterator)]['answer'], inline=False)

        await ctx.send(embed=blank_embed)


def setup(bot):
    bot.add_cog(FAQ(bot))
