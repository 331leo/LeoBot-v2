import discord
from discord.ext import commands
import asyncio
import config
import importlib
import utils.exceptions
#await self.bot.db.guilds.find_one_and_update({"guildId": ctx.guild.id},{"$set":{"member_log_config": {"send_channel":ctx.channel.id,"join_leave":True,"change_nick":False,"change_roles":False}}})
class OnMemberCog(commands.Cog):
    def __init__(self, bot):
        importlib.reload(config)
        self.bot = bot
        self.logger = bot.logger
        self.db = bot.db
    
    async def get_guild_listener_config(self, guild: discord.Guild):
        base_config = {"send_channel":guild.system_channel,"join_leave":True,"change_nick":False,"change_roles":False}
        doc = await self.db.guilds.find_one({"guildId": guild.id})
        if not doc:
            raise utils.exceptions.DB_NO_GUILD_DOCUMENT(self.bot, guild)
        return doc['member_log_config']
        pass
    @commands.command()
    @commands.Cog.listener('on_member_join')
    async def on_member_join(self, member: discord.Member):
        guild_config = await self.get_guild_listener_config(member.guild)
        await ctx.send(str(guild_config))

def setup(bot):
    bot.add_cog(OnMemberCog(bot))