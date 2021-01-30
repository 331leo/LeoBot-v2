import discord
from discord.ext import commands
import importlib
import utils
import config

class UtilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.db = bot.db
        self.check = utils.checks.permissions(bot.db)
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)
            cmds.add_check(self.check.blacklist)
    @commands.command(name="프사")
    async def user_profilepic_command(self, ctx, *, user:discord.User = None):
        """
        사용법: =프사 {유저이름 또는 멘션}
        """
        if not user: user = ctx.author 
        embed = utils.embed_gen.info_embed(f"{user}님의 프로필 사진", "", author=ctx.author)
        embed.set_image(url=str(user.avatar_url))
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UtilCog(bot))