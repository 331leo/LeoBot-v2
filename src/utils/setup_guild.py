import asyncio
import discord

async def setup_guild(bot, guild:discord.Guild):
    base_config = {
        "send_channel": guild.system_channel.id if guild.system_channel else None,
        "join": True,
        "leave": True,
        "change_nick": False,
        "change_roles": False,
        "member_join_description": f"`{guild}`에 오신걸 환영합니다!",
        "member_remove_description": f"`{guild}`에서 나가셨어요ㅠ"
        }
    try:
        await bot.db.guilds.insert_one({"guildId": guild.id, "member_log_config": base_config})
    except Exception as e:
        bot.logger.exception(f"Error on setup_guild: {e}")