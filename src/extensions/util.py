import discord
from discord.ext import commands
import importlib
import config
import hcskr
import utils

class UtilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.db = bot.db
        self.check = utils.checks.permissions(bot.db)


    async def cog_check(self, ctx):
        return await self.check.registered(ctx) and await self.check.blacklist(ctx)
    @commands.command(name="프사",usage=f"유저이름 또는 멘션")
    async def user_profilepic_command(self, ctx, *, user:discord.User = None):
        """
        사용자의 프로필 사진을 확대하여 보여줍니다.
        """
        if not user: user = ctx.author 
        embed = utils.embed_gen.info_embed(f"{user}님의 프로필 사진", "", author=ctx.author)
        embed.set_image(url=str(user.avatar_url))
        
        await ctx.send(embed=embed)
    @commands.command(name="핑", aliases=["ping"])
    async def ping_command(self, ctx):
        """
        봇의 지연시간을 확인합니다.
        """
        text = ""
        if ctx.channel.type != discord.ChannelType.private:
            text += f"`이 서버의 Shard ID: {ctx.guild.shard_id}`\n"
        text += "```"
        for shard in self.bot.shards.values():
            text += f"Shard#{shard.id}: {int(shard.latency*1000)}ms\n"
        text += "```"
        await ctx.send(embed=utils.embed_gen.prompt_embed("Pong!",text))
    @commands.command(name="자가진단")
    async def covid_check_command(self, ctx):
        """
        등록된 정보를 바탕으로 코로나 자가진단을 수행합니다.
        """
        data = await self.db.users.find_one({"discordId": ctx.author.id})
        if not data.get("covid-check", None):
            return await ctx.send(embed=utils.embed_gen.waring_embed(f"{config.NO_EMOJI_STRING}등록된 정보 없음", f"`{config.COMMAND_PREFIXS[0]}자가진단등록` 으로 자가진단 정보를 등록해주세요!", "모든 정보는 안전하게 암호화 되어 보관합니다."))  #등록 정보 없음
        data = await hcskr.asyncTokenSelfCheck(data.get("covid-check", "None"))
        return await ctx.send(embed=utils.embed_gen.success_embed(f"{config.YES_EMOJI_STRING}자가진단 성공!", "", author=ctx.author))

    @commands.command(name="자가진단등록", usage=f"지역 학교급 학교이름 이름 생년월일6자 자가진단비밀번호")
    @commands.dm_only()
    async def register_covid_check_command(self, ctx, area, level, schoolname, name, birthday, password):
        """
        코로나 자가진단 정보를 등록합니다.
        등록하신 정보는 암호화 해서 안전하게 보관합니다.
        """
        data = await hcskr.asyncGenerateToken(name, birthday, area, schoolname, level, password)
        if data['error']:
            return await ctx.send(embed=utils.embed_gen.error_embed(f"{config.NO_EMOJI_STRING}에러", f"{data['message']}"))
        if await utils.update_db(self.bot, "users", {"discordId": ctx.author.id}, {"covid-check": data['token']}):
            return await ctx.send(embed=utils.embed_gen.success_embed(f"{config.YES_EMOJI_STRING}정보 등록 성공!", f"자가진단 정보를 성공적으로 저장하였습니다!\n이제 `{config.COMMAND_PREFIXS[0]}자가진단` 명령어로 [코로나 자가진단](https://hcs.eduro.go.kr)을 수행할수 있어요!", "모든 정보는 안전하게 암호화 되어 보관합니다.", author=ctx.author))



def setup(bot):
    bot.add_cog(UtilCog(bot))