import discord

TOKEN = "NzkxNDAwNjM0NjIzNDU5MzY4.X-OnRg.SBwciY3auUrDV4NhjKAYSoxoLAQ"  # Main Bot

bot = discord.Client()


@bot.event
async def on_ready():
    print("Cyber PYG ready !")


bot.run(TOKEN)
