import discord
from discord.ext import commands
from typing import Optional, Union
import importlib
import utils
from utils import exceptions
import config

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger
        self.check = utils.checks.permissions(bot.db)
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)

    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        self.bot.get_command("가입").remove_check(self.check.registered)
    
    @commands.command(name="가입", aliases=["인증"])
    async def user_register(self, ctx):
        db_user = await self.db.users.find_one({"discordId": ctx.author.id})
        if db_user:
            raise exceptions.PermError.AlreadyRegistered
        msg = await ctx.send(embed=utils.embed_gen.prompt_embed(ctx, "개인정보 처리방침 & 이용약관", f"레오봇을 이용하시려면 [개인정보 처리방침 & 이용약관](https://bot.leok.kr/tos.html) 에 동의하셔야 해요!\n이용약관에 동의하시면 {config.YES_EMOJI_STRING}를 눌러주세요!","60초후 자동으로 취소됩니다",author=True))
        if await utils.interface.is_confirmed(ctx, msg):
            result = await utils.setup_user(self.bot, ctx.author)
            if result:
                return await ctx.send(embed=utils.embed_gen.success_embed(ctx, f"{config.YES_EMOJI_STRING} 가입 성공!", f"이제 레오봇의 모든 기능을 이용햘수 있어요!\n`{config.COMMAND_PREFIXS[0]}도움말` 로 레오봇의 기능을 알아보세요!",author=True))
        else:
            return await ctx.send(embed=utils.embed_gen.info_embed(ctx,f"{config.NO_EMOJI_STRING} 가입 취소됨", f"레오봇 가입을 취소하였습니다.\n`{config.COMMAND_PREFIXS[0]}가입`을 통해 다시 가입 창을 띄울수 있어요!",author=True))


def setup(bot):
    bot.add_cog(UserCog(bot))