import datetime
import config
import discord
import utils
from typing import Optional, Union
from discord.ext import commands
KST = datetime.timedelta(hours=9)
        

def member_join(member, guild_config):
    embed = discord.Embed(title=f"{member} 님이 들어오셨어요!",
                          description=f"{guild_config['member_join_description']}",
                          color=utils.colormap["aqua"],
                          timestamp=datetime.datetime.utcnow()
                          )
    embed.set_thumbnail(url=f"{str(member.avatar_url)}")
    embed.add_field(name="계정 생성일", value=f"{str(member.created_at + KST)[:-10]}", inline=True)
    embed.set_footer(text=f"멤버로그 설정: {config.COMMAND_PREFIXS[0]}멤버로그")
    return embed
def member_remove(member, guild_config):
    embed = discord.Embed(title=f"{member}님이 나가셨어요:cry:",
                          description=f"{guild_config['member_remove_description']}",
                          color=utils.colormap["hotpink"],
                          timestamp=datetime.datetime.utcnow()
                          )
    embed.set_thumbnail(url=f"{str(member.avatar_url)}")
    embed.add_field(name='계정 생성일', value=f'{str(member.created_at + KST)[:-10]}', inline=True)
    embed.add_field(name='서버 참가일', value=f'{str(member.joined_at + KST)[:-10]}', inline=True)
    embed.set_footer(text=f"멤버로그 설정: {config.COMMAND_PREFIXS[0]}멤버로그")
    return embed
def member_nick_change(member_before, member_after, guild_config):
    embed = discord.Embed(title=f"별명 변경",
                          description=f"**{member_after.mention}님의 별명**\n`{member_before.display_name}`:arrow_right: `{member_after.display_name}`",
                          color=utils.colormap['yellowgreen'],
                          timestamp=datetime.datetime.utcnow()
                          )
    embed.set_footer(text=f"멤버로그 설정: {config.COMMAND_PREFIXS[0]}멤버로그")
    return embed

def member_roles_change(member_before, member_after, guild_config):
    roles_removed = list(set(member_before.roles) - set(member_after.roles))
    roles_added = list(set(member_after.roles) - set(member_before.roles))
    text = ""
    for role in roles_removed:
        text += f"제거됨{config.NO_EMOJI_STRING}: {role.mention}\n"
    for role in roles_added:
        text+=f"추가됨{config.YES_EMOJI_STRING}: {role.mention}\n"
    embed = discord.Embed(title=f"역할 변경",
                          description=f"**{member_after.mention} 님의 역할**\n"+text,
                          color=utils.colormap['yellowgreen'],
                          timestamp=datetime.datetime.utcnow()
                          )
    embed.set_footer(text=f"멤버로그 설정: {config.COMMAND_PREFIXS[0]}멤버로그")
    return embed

def NoUserPerm(ctx, perm):
    embed = discord.Embed(title=f"{config.NO_EMOJI_STRING} 유저 권한 부족",
                          description=f"{ctx.author.mention}님은 `{ctx.command}` 명령어를 실행할 권한이 없습니다.",
                          color=utils.colormap['red'],
                          timestamp=datetime.datetime.utcnow()
                          )
    embed.set_footer(text=f"`{perm}` 권한 필요")
    return embed
def NoBotPerm(ctx, perm):
    embed = discord.Embed(title=f"{config.NO_EMOJI_STRING} 봇 권한 부족",
                          description=f"그 작업을 실행하기에 {ctx.guild.me.mention}은 너무 작고 하찮습니다..",
                          color=utils.colormap['red'],
                          timestamp=datetime.datetime.utcnow()
                          )
    embed.set_footer(text=f"`{perm}` 권한 필요")
    return embed
def success_embed(title: str, description: str, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=utils.colormap['lightgreen'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:
        embed.set_footer(text=footer)
    return embed
def prompt_embed(title: str, description: str, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=utils.colormap['yellow'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:  
        embed.set_footer(text=footer)
    return embed
def info_embed(title: str, description: str, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=utils.colormap['skyblue'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:
        embed.set_footer(text=footer)
    return embed
def error_embed(title: str, description: str, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=utils.colormap['red'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:
        embed.set_footer(text=footer)
    return embed
def waring_embed(title: str, description: str, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=utils.colormap['lightpink'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:
        embed.set_footer(text=footer)
    return embed