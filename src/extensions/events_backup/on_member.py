import discord
from discord.ext import commands
import asyncio
import config
import importlib
from utils import exceptions
import utils
import template.event_embed_gen
#await self.bot.db.guilds.find_one_and_update({"guildId": ctx.guild.id},{"$set":{"member_log_config": {"send_channel":ctx.channel.id,"join_leave":True,"change_nick":False,"change_roles":False}}})
class OnMemberCog(commands.Cog):
    def __init__(self, bot):
        importlib.reload(config)
        self.bot = bot
        self.logger = bot.logger
        self.db = bot.db
        print("READY")
        
    async def get_guild_listener_config(self, guild: discord.Guild):
        base_config = {"send_channel":guild.system_channel,"join_leave":True,"change_nick":False,"change_roles":False}
        doc = await self.db.guilds.find_one({"guildId": guild.id})
        if not doc:
            raise exceptions.DB_NO_GUILD_DOCUMENT(self.bot, guild)
        return doc['member_log_config']
        pass

    @commands.Cog.listener('on_member_join')
    async def on_member_join(self, member: discord.Member):
        guild_config = await self.get_guild_listener_config(member.guild)
        if guild_config['join']:
            await self.bot.get_channel(guild_config['send_channel']).send(embed=template.event_embed_gen.member_join(member,guild_config))
    
    @commands.Cog.listener('on_member_remove')
    async def on_member_remove(self, member: discord.Member):
        guild_config = await self.get_guild_listener_config(member.guild)
        if guild_config['remove']:
            await self.bot.get_channel(guild_config['send_channel']).send(embed=template.event_embed_gen.member_remove(member,guild_config))

    @commands.Cog.listener('on_member_update')
    async def on_member_update(self, member_before: discord.Member, member_after: discord.Member):
        print("MEMBER UPDATE CATCH")
        guild_config = await self.get_guild_listener_config(member.guild)
        if guild_config['change_nick'] and member_before.display_name != member_after.display_name:
            await self.bot.get_channel(guild_config['send_channel']).send(embed=template.event_embed_gen.member_nick_change(member_before,member_after,guild_config))
        if guild_config['change_role'] and member_before.roles != member_after.roles:
            pass

def setup(bot):
    bot.add_cog(OnMemberCog(bot))