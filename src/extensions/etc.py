import discord
from discord.ext import commands
from typing import Optional, Union
import importlib
import utils
from utils import exceptions
import config
import string
import random
import datetime
class EtcCog(commands.Cog):
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
        '''
        이용자 가입 명령어
        '''
        db_user = await self.db.users.find_one({"discordId": ctx.author.id})
        if db_user:
            raise exceptions.PermError.AlreadyRegistered
        msg = await ctx.send(embed=utils.embed_gen.prompt_embed("개인정보 처리방침 & 이용약관", f"레오봇을 이용하시려면 [개인정보 처리방침 & 이용약관](https://bot.leok.kr/tos.html) 에 동의하셔야 해요!\n이용약관에 동의하시면 {config.YES_EMOJI_STRING}를 눌러주세요!","60초후 자동으로 취소됩니다",author=ctx.author))
        if await utils.interface.is_confirmed(ctx, msg):
            result = await utils.setup_user(self.bot, ctx.author)
            if result:
                return await ctx.send(embed=utils.embed_gen.success_embed(f"{config.YES_EMOJI_STRING} 가입 성공!", f"이제 레오봇의 모든 기능을 이용햘수 있어요!\n`{config.COMMAND_PREFIXS[0]}도움말` 로 레오봇의 기능을 알아보세요!",author=ctx.author))
        else:
            return await ctx.send(embed=utils.embed_gen.info_embed(f"{config.NO_EMOJI_STRING} 가입 취소됨", f"레오봇 가입을 취소하였습니다.\n`{config.COMMAND_PREFIXS[0]}가입`을 통해 다시 가입 창을 띄울수 있어요!", author=ctx.author))
    
    @commands.command(name="문의", aliases=["건의"], usage=f"문의할내용")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def contect_support(self, ctx, *, text):
        """
        봇 개발자에게 문의를 전달합니다.
        """
        if len(text) < 10:
             await ctx.send(embed=utils.embed_gen.waring_embed(f"{config.NO_EMOJI_STRING} 문의 오류!", f"문의가 너무 짧습니다!\n조금 더 길게 적어주세요!", "최소 10자", ctx.author))
             return ctx.command.reset_cooldown(ctx)
        supportId=utils.random_string(6)
        success = await utils.update_db(self.bot, "support", {"supportId": supportId}, {"supportId": supportId, "message": text, "user": ctx.author.id, "timestamp": datetime.datetime.now()})
        await self.bot.get_channel(config.SUPPORT_LOG_CHANNEL).send(embed=utils.embed_gen.info_embed(f"문의코드: {supportId}",f"{ctx.author.mention}님이 보내신 문의입니다.\n```{text}```",f"{config.COMMAND_PREFIXS[0]}답변 <문의코드> <내용> 으로 답변",author=ctx.author))
        return await ctx.send(embed=utils.embed_gen.success_embed(f"{config.YES_EMOJI_STRING} 문의 성공!", f"성공적으로 개발자에게 문의사항을 전달했습니다!\n답변은 DM으로 전송됩니다!", f"문의코드: {supportId}",author=ctx.author))

def setup(bot):
    bot.add_cog(EtcCog(bot))