import asyncio
import discord

async def setup_guild(bot, guild:discord.Guild):
    base_config = {"send_channel": guild.system_channel.id, "join_leave": True, "change_nick": False, "change_roles": False}
    try:
        await bot.db.guilds.insert_one({"guildId": guild.id, "member_log_config": base_config})
    except Exception as e:
        bot.logger.exception(f"Error on setup_guild: {e}")