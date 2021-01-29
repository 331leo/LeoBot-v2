import discord
import asyncio
from discord.ext import commands

class DB_NO_GUILD_DOCUMENT(Exception):
    def __init__(self, bot, guild):
        bot.logger.exception(f"No such DB Document for: {guild.name}, {guild.id}")
        super().__init__(f"No DB Document for: {guild.name}, {guild.id}")

class PermError:
    class NotRegistered(commands.CheckFailure):
        def __str__(self):
            return "Not registered User"
    class NotBotMaster(commands.CheckFailure):
        def __str__(self):
            return "Not Master User"
    class BlacklistedUser(commands.CheckFailure):
        def __str__(self):
            return "BlackListed User"
    class AlreadyRegistered(commands.CheckFailure):
        def __str__(self):
            return "Already Registered User"
    