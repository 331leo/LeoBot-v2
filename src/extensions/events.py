import discord
from discord.ext import commands, tasks
import asyncio
import config
import importlib
from utils import exceptions
import utils
from itertools import cycle
import datetime
#await self.bot.db.guilds.find_one_and_update({"guildId": ctx.guild.id},{"$set":{"member_log_config": {"send_channel":ctx.channel.id,"join_leave":True,"change_nick":False,"change_roles":False}}})
class EventsCog(commands.Cog):
    def __init__(self, bot):
        importlib.reload(config)
        self.bot = bot
        self.logger = bot.logger
        self.db = bot.db
        self.statusList = cycle(config.BOT_STATUS)
        self.change_bot_status.start()
    
    #봇 커스텀 상태 표시 함수
    @tasks.loop(seconds=10)
    async def change_bot_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.statusList).format(version=self.bot.version, server_count=len(self.bot.guilds), user_count=len(self.bot.users))))
    

    #커멘드 에러 핸들러
    @commands.Cog.listener('on_command_error')
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        print(error)
        if isinstance(error, exceptions.PermError.NotRegistered):
            self.logger.info(f"Not Registered User: {ctx.author.id}")
            await ctx.send(embed=discord.Embed(title="가입이 필요합니다.",description="레오봇의 모든 기능을 이용하시려면,\n`=가입` 명령어를 통해 레오봇에 가입해주세요!",color=utils.colormap['aqua'],timestamp=datetime.datetime.utcnow()))
            return
        
        if isinstance(error, exceptions.PermError.NotBotMaster):
            await ctx.send(embed=utils.embed_gen.NoUserPerm(ctx, "BotMaster"))
            return

    #멤버 이벤트 헨들러
    async def get_guild_listener_config(self, guild: discord.Guild):
        base_config = {"send_channel":guild.system_channel,"join_leave":True,"change_nick":False,"change_roles":False}
        doc = await self.db.guilds.find_one({"guildId": guild.id})
        if not doc:
            raise exceptions.DB_NO_GUILD_DOCUMENT(self.bot, guild)
        return doc['member_log_config']
        pass

    def format_guild_config(self, guild_config, guild: discord.Guild):
        kwargs = {"system_channel": guild.system_channel.id if guild.system_channel else 0, "guild_name": guild.name}
        formated_send_channel = str(guild_config['send_channel']).format(**kwargs)
        formated_member_join_description = str(guild_config['member_join_description']).format(**kwargs)
        foramted_member_remove_description = str(guild_config['member_remove_description']).format(**kwargs)
        guild_config.update({"send_channel": int(formated_send_channel), "member_join_description": formated_member_join_description, "member_remove_description": foramted_member_remove_description})
        return guild_config

    @commands.Cog.listener('on_member_join')
    async def on_member_join(self, member: discord.Member):
        guild_config = self.format_guild_config(await self.get_guild_listener_config(member.guild),member.guild)
        formated_send_channel=str(guild_config['send_channel']).format(system_channel=member.guild.system_channel)
        if guild_config['join']:
            await self.bot.get_channel(guild_config['send_channel']).send(embed=utils.embed_gen.member_join(member,guild_config))
    
    @commands.Cog.listener('on_member_remove')
    async def on_member_remove(self, member: discord.Member):
        guild_config = self.format_guild_config(await self.get_guild_listener_config(member.guild),member.guild)
        if guild_config['remove']:
            await self.bot.get_channel(guild_config['send_channel']).send(embed=utils.embed_gen.member_remove(member,guild_config))

    @commands.Cog.listener('on_member_update')
    async def on_member_update(self, member_before: discord.Member, member_after: discord.Member):
        if member_before.display_name != member_after.display_name and member_before.bot == False:
            guild_config = self.format_guild_config(await self.get_guild_listener_config(member_before.guild),member_before.guild)
            if guild_config['change_nick']:
                await self.bot.get_channel(guild_config['send_channel']).send(embed=utils.embed_gen.member_nick_change(member_before, member_after, guild_config))
        if member_before.roles != member_after.roles:
            guild_config = self.format_guild_config(await self.get_guild_listener_config(member_before.guild),member_before.guild)
            if guild_config['change_roles']:
                pass

def setup(bot):
    bot.add_cog(EventsCog(bot))