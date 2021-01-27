import discord
from discord.ext import commands
from typing import Optional, Union
import importlib
import utils
from utils import exceptions

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger

        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)
    
    @commands.command(name="가입", aliases=["인증"])
    async def user_register(self, ctx):
        await ctx.send()
        result = await utils.setup_user(self.bot, ctx.author)
        if result:
            await ctx.send(embed=utils.embed_gen.success_embed(ctx, "가입 성공!"))


def setup(bot):
    bot.add_cog(UserCog(bot))