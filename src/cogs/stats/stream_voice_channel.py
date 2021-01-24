from typing import Union

import discord
from discord.ext import commands


class Stream_VC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        """ Voice User State Update """

        user_channel = member.voice.channel if member.voice else False
        old_name: str = after.channel.name
        print(f"Old name = {old_name}")

        if before.channel and after.channel:  # User's connected before and after the update
            print(f"Stream : {after.self_stream}")

            if after.self_stream:  # If user's currently streaming
                if "Salon de" in after.channel.name:  # If the channel's a private one
                    old_name = user_channel.name
                    game_activity = None

                    """ Check throughout the different activities the user may have """
                    for i in range(len(member.activities)):
                        if member.activities[i].type.__eq__(discord.ActivityType.playing):
                            game_activity = member.activities[i]

                    print(game_activity.name)
                    # todo: Le print d'au-dessus fonctionne, mais le user channel ne semble pas éditer, ou une fois sur deux, protection de l'API ?
                    await user_channel.edit(name=f"{game_activity.name} - {member.name}")

            else:  # User stop streaming [stable]
                print(2)
                await user_channel.edit(name=old_name)
        elif not user_channel:  # User leaves channel
            # todo: L'user channel est déjà null, l'événement trigger après que le membre quitte, il faudrait pouvoir récupérer le channel via le bot guild
            print(3)
            # await user_channel.edit(name=old_name)


def setup(bot):
    bot.add_cog(Stream_VC(bot))
