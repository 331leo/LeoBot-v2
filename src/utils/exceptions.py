import discord
import asyncio

class DB_NO_GUILD_DOCUMENT(Exception):
    def __init__(self, bot, guild):
        bot.logger.exception(f"No such DB Document for: {guild.name}, {guild.id}")
        super().__init__(f"No DB Document for: {guild.name}, {guild.id}")