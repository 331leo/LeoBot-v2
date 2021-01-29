import os
from datetime import datetime
import importlib
import logging
import psutil
import discord
import config
from discord.ext import commands
import traceback
from utils.interface import is_confirmed
import utils
import typing 
class AdminCog(commands.Cog):
    def __init__(self, bot):
        importlib.reload(config)
        self.db = bot.db
        self.logger = bot.logger
        self.bot = bot
        self.check = utils.checks.permissions(bot.db)
        
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)
            cmds.add_check(self.check.master)
        
        
    @commands.command(name="reload", aliases=["리로드"], brief="모듈 핫리로드")
    async def reload(self, ctx: commands.Context, path):
        if path == "*":
            for path in config.EXTENSION_LIST:
                await ctx.send(f"{path} 모듈을 리로드 하는중...")
                self.bot.reload_extension(path)
        else:
            await ctx.send(f"extensions.{path} 모듈을 리로드 하는중...")
            self.bot.reload_extension(f"extensions.{path}")
        await ctx.send(f"모듈 리로드 성공")
    @commands.command(name="강제초기설정")
    async def force_init_bot(self, ctx: commands.Context):
        for guild in self.bot.guilds:
            await ctx.send(await utils.setup_guild(self.bot,guild))

    @commands.command(name="uptime", aliases=["업타임"], brief="업타임")
    async def uptime(self, ctx: commands.Context):
        now = datetime.now()
        server_uptime = now - datetime.fromtimestamp(psutil.boot_time())
        python_uptime = now - datetime.fromtimestamp(
            psutil.Process(os.getpid()).create_time()
        )

        await ctx.send(
            f"**Bot Uptime** {python_uptime}"
        )

    @commands.command(name="shutdown", aliases=["종료"], brief="봇 종료")
    async def shutdown(self, ctx: commands.Context):
        prompt = await ctx.send("봇을 종료할까요?")
        if await is_confirmed(ctx, prompt):
            await ctx.send("ㅂㅇ")
            await ctx.bot.logout()
    @commands.command(name='eval')
    async def _eval(self, ctx: commands.Context, *, arg):
        try:
            rst = eval(arg)
        except:
            evalout = f'📥INPUT: ```python\n{arg}```\n💥EXCEPT: ```python\n{traceback.format_exc()}```\n ERROR'
            print(traceback.format_exc())
            
        else:
            evalout = f'📥INPUT: ```python\n{arg}```\n📤OUTPUT: ```python\n{rst}```\n SUCCESS'
            print(rst)
        embed=discord.Embed(title='**💬 EVAL**', description=evalout)
        await ctx.send(embed=embed)

    @commands.command(name='exec')
    async def _exec(self, ctx: commands.Context, *, arg):
        try:
            exec(arg)
        except:
            evalout = f'📥INPUT: ```python\n{arg}```\n💥EXCEPT: ```python\n{traceback.format_exc()}```\n ERROR'
            print(traceback.format_exc())
            
        else:
            evalout = f'📥INPUT: ```python\n{arg}```\n SUCCESS'
            
        embed=discord.Embed(title='**💬 EXEC**',  description=evalout)
        await ctx.send(embed=embed)

    @commands.command(name='await')
    async def _await(self, ctx: commands.Context, *, arg):
        try:
            rst = await eval(arg)
        except:
            evalout = f'📥INPUT: ```python\n{arg}```\n💥EXCEPT: ```python\n{traceback.format_exc()}```\n ERROR'
            print(traceback.format_exc())
            
        else:
            evalout = f'📥INPUT: ```python\n{arg}```\n📤OUTPUT: ```python\n{rst}```\n SUCCESS'
            print(rst)
            
        embed=discord.Embed(title='**💬 AWAIT**',  description=evalout)
        await ctx.send(embed=embed)
    #DB업데이트 테스트
    @commands.command(name="답변")
    async def support_reply(self, ctx: commands.Context, supportId: str, *, text):
        supportData = await self.db.support.find_one({"supportId": supportId})
        if not supportData:
            return await ctx.send(embed=utils.embed_gen.error_embed(f"{config.NO_EMOJI_STRING} 올바르지 않은 문의코드", "올바른 문의코드를 입력하였는지 다시 한번 확인해주세요!"))
        supportUser = self.bot.get_user(supportData['user'])
        if not supportUser:
            return await ctx.send(embed=utils.embed_gen.error_embed(f"{config.NO_EMOJI_STRING} 에러", f"찾을 수 없는 이용자입니다.(레오봇과 공통된 서버 없음)"))
        text_splited = text.split("\n")
        text_splited.insert(0,"")
        text = "\n> ".join(text_splited)
        userEmbed = utils.embed_gen.info_embed(f"문의 답변", f"""```\n{supportData['message']}\n```{text}""", f"문의코드: {supportId}", author=ctx.author)
        msg = await ctx.send(f"이 내용을 {supportUser}({supportUser.mention}) 님께 전달할까요?", embed=userEmbed)
        if await is_confirmed(ctx, msg):
            try:
                await supportUser.send(embed=userEmbed)
            except:
                return await msg.edit(content="",embed=utils.embed_gen.error_embed(f"{config.NO_EMOJI_STRING} 에러",f"{supportUser}({supportUser.mention}) 님이 개인 DM을 차단하셔서 메세지 전송에 실패하였습니다."))
            return await msg.edit(content="",embed=utils.embed_gen.success_embed(f"{config.YES_EMOJI_STRING} 답변 발송 성공!",f"{supportUser}({supportUser.mention}님에게\n문의에 대한 답변을 성공적으로 발송하였습니다!",f"문의코드: {supportId}"))
        else:
            return await msg.edit(content="",embed=utils.embed_gen.error_embed(f"{config.NO_EMOJI_STRING} 취소되었습니다",""))

        

def setup(bot):
    bot.add_cog(AdminCog(bot))
