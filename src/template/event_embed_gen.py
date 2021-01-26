import datetime
import config
import discord
import utils
KST = datetime.timedelta(hours=9)

def member_join(member, guild_config):
    embed = discord.Embed(title=f"{member} 님이 들어오셨어요!",
                          description=f"{guild_config['member_join_description'].format(guild_name=member.guild.name)}",
                          color=utils.colormap["aqua"],
                          timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=f"{str(member.avatar_url)}")
    embed.add_field(name="계정 생성일", value=f"{str(member.created_at + KST)[:-10]}", inline=True)
    embed.set_footer(text=f"멤버로그 설정: {config.COMMAND_PREFIXS[0]}멤버로그")
    return embed
def member_remove(member, guild_config):
    embed = discord.Embed(title=f"{member}님이 나가셨어요:cry:",
                          description=f"{guild_config['member_remove_description'].format(guild_name=member.guild.name)}",
                          color=utils.colormap["hotpink"],
                          timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=f"{str(member.avatar_url)}")
    embed.add_field(name='계정 생성일', value=f'{str(member.created_at + KST)[:-10]}', inline=True)
    embed.add_field(name='서버 참가일', value=f'{str(member.joined_at + KST)[:-10]}', inline=True)
    embed.set_footer(text=f"멤버로그 설정: {config.COMMAND_PREFIXS[0]}멤버로그")
    return embed