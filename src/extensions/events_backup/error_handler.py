import discord
from discord.ext import commands
class ErrorHandlerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.db = bot.db

    @commands.Cog.listener('on_command_error')
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        pass

def setup(bot):
    bot.add_cog(ErrorHandlerCog(bot))