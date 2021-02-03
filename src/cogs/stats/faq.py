from discord import Embed
from discord.ext import commands
from utils import safe_delete, load_faq, write_data_to_faq
import unicodedata

import pprint


class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='spawn_faq')
    async def activity(self, ctx):
        await safe_delete(ctx)
        data: list = load_faq()

        blank_embed = Embed(
            description="Et si vous portiez un peu d'attention aux questions les plus posées sur P-Y-G ?\n",
            color=0x2F3136)

        for iterator in data:
            blank_embed.add_field(name=f"**{iterator['question']}** + {iterator['reaction']}",
                                  value=iterator['answer'], inline=False)

        bot_message = await ctx.send(embed=blank_embed)

        for iterator in data:
            await bot_message.add_reaction(iterator['reaction'])

    @commands.command(name='add_faq')
    async def add_faq(self, ctx):
        author = ctx.author
        await safe_delete(ctx)

        await ctx.send("Quelle question souhaitez-vous ajouter ?")
        question = await self.bot.wait_for('message', check=lambda msg: msg.author == author)

        await ctx.send("Quelle est la réponse de cette question ?")
        answer = await self.bot.wait_for('message', check=lambda msg: msg.author == author)

        await ctx.send("Et enfin, quelle réaction pour ce beau couple ? (Ajouter un emoji en réaction de ce message)")
        reaction, user = await self.bot.wait_for('reaction_add', check=lambda reac, user: user == author)

        write_data_to_faq(question.content, answer.content, str(reaction.emoji))
        await ctx.send("Merci ! Tout a été ajouté !")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id is not None:
            pass  # todo: Mettre quelque chose pour vérifier que le message où on ajoute la réaction est bien celui du FAQ


def setup(bot):
    bot.add_cog(FAQ(bot))
