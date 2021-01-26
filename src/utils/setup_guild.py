import asyncio
import discord

async def setup_guild(bot, guild:discord.Guild):
    base_config = {
        "send_channel": "{system_channel}",
        "join": True,
        "remove": True,
        "change_nick": False,
        "change_roles": False,
        "member_join_description": "`{guild_name}`에 오신걸 환영합니다!",
        "member_remove_description": "`{guild_name}`에서 나가셨어요ㅠ"
        }
    try:
        await bot.db.guilds.insert_one({"guildId": guild.id, "member_log_config": base_config})
        return {"guildId": guild.id}
    except Exception as e:
        bot.logger.exception(f"Error on setup_guild: {e}")