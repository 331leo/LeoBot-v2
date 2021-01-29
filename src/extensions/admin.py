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
    async def reload(self, ctx, path):
        if path == "*":
            for path in config.EXTENSION_LIST:
                await ctx.send(f"{path} 모듈을 리로드 하는중...")
                self.bot.reload_extension(path)
        else:
            await ctx.send(f"extensions.{path} 모듈을 리로드 하는중...")
            self.bot.reload_extension(f"extensions.{path}")
        await ctx.send(f"모듈 리로드 성공")
    @commands.command(name="강제초기설정")
    async def force_init_bot(self, ctx):
        for guild in self.bot.guilds:
            await ctx.send(await utils.setup_guild(self.bot,guild))

    @commands.command(name="uptime", aliases=["업타임"], brief="업타임")
    async def uptime(self, ctx):
        now = datetime.now()
        server_uptime = now - datetime.fromtimestamp(psutil.boot_time())
        python_uptime = now - datetime.fromtimestamp(
            psutil.Process(os.getpid()).create_time()
        )

        await ctx.send(
            f"**Bot Uptime** {python_uptime}"
        )

    @commands.command(name="shutdown", aliases=["종료"], brief="봇 종료")
    async def shutdown(self, ctx):
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
    @commands.command()
    async def test(self, ctx):
        await ctx.send(await utils.update_db(self.bot,{"guildId": ctx.guild.id}, {"change_roles": True}, "member_log_config"))

def setup(bot):
    bot.add_cog(AdminCog(bot))
