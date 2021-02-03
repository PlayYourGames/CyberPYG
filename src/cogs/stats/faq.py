from discord.ext import commands


class FAQ(commands.Cog):
    pass


def setup(bot):
    bot.add_cog(FAQ(bot))
