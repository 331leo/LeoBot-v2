import discord
from discord.ext import commands
import motor.motor_asyncio
from . import exceptions
class permissions:
    def __init__(self, db: motor.motor_asyncio.AsyncIOMotorClient):
        self.db = db
    
    async def registered(self, ctx):
        db_user = await self.db.users.find_one({"discordId": ctx.author.id})
        if db_user:
            return True
        raise exceptions.PermError.NotRegistered

    async def master(self, ctx):
        db_user = await self.db.users.find_one({"discordId": ctx.author.id})
        if not db_user:
            raise exceptions.PermError.NotRegistered
        if not db_user['flags']['master']:
            raise exceptions.PermError.NotBotMaster
        return True

    async def blacklist(self, ctx):
        db_user = await self.db.users.find_one({"discordId": ctx.author.id})
        if not db_user:
            raise exceptions.PermError.NotRegistered
        if db_user['flags']['ban']:
            raise exceptions.PermError.BlacklistedUser
        return True
    
