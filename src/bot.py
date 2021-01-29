import json
import logging
import logging.config
import os
import discord
from discord.ext import commands
import config
import motor.motor_asyncio
import koreanbots
with open("logging.json") as f:
    logging.config.dictConfig(json.load(f))


class LeoBot(commands.AutoShardedBot):

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user}, Bot Version {config.VERSION}")


    def __init__(self, logger):
        intents = discord.Intents.default()
        intents.members = config.BOT_INTENT_MEMBERS
        intents.presences = config.BOT_INTENT_PRESENCES
        super().__init__(commands.when_mentioned_or(*config.COMMAND_PREFIXS), intents=intents)
        self.logger = logger
        self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{config.MONGO_DB_USERNAME}:{config.MONGO_DB_PASSWORD}@{config.MONGO_DB_HOST}:{config.MONGO_DB_PORT}")
        self.db = self.dbclient.LeoBot
        self.version = config.VERSION
        self.logger.info(f"Successfully Connected to mongodb://{config.MONGO_DB_USERNAME}:*******@{config.MONGO_DB_HOST}:{config.MONGO_DB_PORT}")
        self.KBClient = koreanbots.Client(self, config.KOREAN_BOTS_TOKEN)
        for ext in config.EXTENSION_LIST:
            self.load_extension(ext)
            



bot = LeoBot(logger=logging.getLogger("bot"))


bot.run(config.BOT_TOKEN)
