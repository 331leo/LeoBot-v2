from discord.ext import commands, tasks
from itertools import cycle
import discord
import config
class change_presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger
        self.statusList = cycle(config.BOT_STATUS)
        self.change_bot_status.start()
        
    @tasks.loop(seconds=10)
    async def change_bot_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.statusList).format(version=self.bot.version, server_count=len(self.bot.guilds), user_count=len(self.bot.users))))

def setup(bot):
    bot.add_cog(change_presence(bot))