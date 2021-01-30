import discord
from discord.ext import commands
import importlib
import utils
import config

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.db = bot.db
        self.check = utils.checks.permissions(bot.db)
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)
            cmds.add_check(self.check.blacklist)

    
    @commands.command(name="testcommand")
    @commands.has_guild_permissions(administrator=True)
    async def testcommand(self, ctx):
        await ctx.send(ctx.author.mention)

def setup(bot):
    bot.add_cog(ModerationCog(bot))