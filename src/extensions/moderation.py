import discord
from discord.ext import commands
import importlib
import utils
import config
import asyncio
import datetime
from typing import Union, Optional
class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.db = bot.db
        self.check = utils.checks.permissions(bot.db)
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)
            cmds.add_check(self.check.blacklist)

    @commands.group(name="경고")
    async def g_warn(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send("존재하지 않는 서브커멘드입니다.")

    @commands.command(name="testcommand")
    @commands.has_guild_permissions(administrator=True)
    async def testcommand(self, ctx):
        await ctx.send(ctx.author.mention)

    @commands.command(name="정리", usage=f"갯수 (유저이름/멘션)")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def purge_message_command(self, ctx, purge_count: int, *, user: Optional[discord.User] = None):
        """
        메세지를 보낸 채널에서 '갯수' 만큼의 메세지를 정리합니다.
        갯수 뒤에 유저를 지정할 경우 해당 유저가 보낸 메세지만 삭제합니다.
        """
        def check(m):
            if user:
                return m.author == user
            return True
        await ctx.channel.purge(limit=purge_count + 1,check=check)
        if user:
            msg = await ctx.send(embed=utils.embed_gen.success_embed(f"{config.YES_EMOJI_STRING}메세지 정리 완료!", f"{user.mention}님이 보내신 메세지 {purge_count}개를 정리하였습니다!","5초후 자동 삭제됩니다!"))
            await asyncio.sleep(5)
            return await msg.delete()
        msg = await ctx.send(embed=utils.embed_gen.success_embed(f"{config.YES_EMOJI_STRING}메세지 정리 완료!", f"메세지 {purge_count}개를 정리하였습니다!", "5초후 자동 삭제됩니다!"))
        await asyncio.sleep(5)
        return await msg.delete()
    
    @commands.command(name="킥", usage="유저이름/멘션 (사유)")
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick_command(self, ctx, user: discord.User, *, reason: Optional[str] = None):
        try:
            await user.kick(reason=reason)
            await ctx.send(embed=utils.embed_gen.prompt_embed(f"{config.YES_EMOJI_STRING}킥 성공!", f"사유: ```{reason}``` {user.mention}님을 `{ctx.guild}`에서 추방했습니다."))
        except:
            raise commands.BotMissingPermissions(["봇의 역할이 대상보다 높은 역할"]) 
    @g_warn.command(name="추가", usage="유저이름/멘션 (사유)")
    @commands.has_guild_permissions(kick_members=True)
    async def warn_add(self, ctx, user:discord.User, *, reason:Optional[str] = None):
        """
        유저에 대한 경고를 추가합니다.
        """
        code = utils.random_string(6)
        data = await self.db.guilds.find_one({"guildId": ctx.guild.id})
        if data['warnings'].get(str(user.id),None):
            data['warnings'][str(user.id)].update({code: {"reason": reason, "created_at": datetime.datetime.now()}})
        else:
            data['warnings'].update({str(user.id):{code: {"reason": reason, "created_at": datetime.datetime.now()}}})
        await self.db.guilds.find_one_and_replace({"guildId": ctx.guild.id}, data)
        
        await ctx.send(embed=utils.embed_gen.waring_embed(f"{config.YES_EMOJI_STRING}경고 추가 성공!", f"사유: ```{reason}``` {user.mention}님에게 경고를 추가하였습니다.\n총 경고 수는 {len(data['warnings'][str(user.id)])}회 입니다.", f"{data['warn_count_config']}회 경고시 자동 킥"))
        
        if len(data['warnings'][str(user.id)]) >= data['warn_count_config']:
            if commands.bot_has_guild_permissions(kick_members=True):
                try:
                    await user.kick()
                except:
                    raise commands.BotMissingPermissions(["봇의 역할이 대상보다 높은 역할"]) 
    
        
def setup(bot):
    bot.add_cog(ModerationCog(bot))