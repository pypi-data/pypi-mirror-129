from .cog import *
from .constants import *
from discord.ext import commands

def register_commands(
    bot,
    *,
    ignore: list = []
):
    games = [
        game for game in ALL_GAMES if game not in ignore
    ]
    class Games(*games):
        pass
    bot.add_cog(Games(bot))
