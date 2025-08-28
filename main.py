import discord
from discord.ext import commands,tasks
from discord import app_commands
import datetime
import pytz
import asyncio
import re

intents = discord.Intents.all() 
session = discord.Client(intents=intents,allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
tree = app_commands.CommandTree(session)
token=""
guilds={}
normal_times={
    '00:00',
    '02:00',
    '04:00',
    '06:00',
    '08:00',
    '10:00',
    '12:00',
    '14:00',
    '16:00',
    '18:00',
}

async def nuker(guildid):
    guild = session.get_guild(int(guildid))
    for channel in guild.text_channels:
        if not channel.topic==None:
            if 'channelresetter' in channel.topic:
                print(channel.topic)
                times=re.search(r"reset_time\[(\d+:\d+)(?:,(\d+:\d+))*\]",channel.topic)
                times_list=normal_times
                if times:
                    times_list = times.groups()
                now = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
                if now in times_list:
                    position = channel.position
                    await channel.delete()
                    resetedchannel = await channel.clone()
                    await resetedchannel.edit(position=position)
                    embed = discord.Embed(title='チャンネルをリセットしました',description='サポートアカウント:[@zrpy0](https://x.com)', timestamp=datetime.datetime.now(pytz.timezone('Asia/Tokyo')))
                    embed.set_footer(text=f"Produced by @zrpy0", icon_url=session.user.display_avatar.url)
                    await resetedchannel.send(embed=embed)

@tasks.loop(seconds=60)
async def nukeloops():
    tasks=[]
    for guildid in guilds:
        tasks.append(asyncio.create_task(nuker(guildid)))
    await asyncio.gather(*tasks)

@session.event
async def on_ready():
    nukeloops.start()
    await tree.sync()

@tree.command(name="add_reset",description="チャンネルログ削除を設定するよ")
@commands.has_guild_permissions(manage_guild=True,manage_channels=True)
async def add_reset(ctx):
    if ctx.guild.id in guilds:
        await ctx.response.send_message("設定しています")
        return
    guilds[ctx.guild.id]={}
    await ctx.response.send_message("設定しました")

@tree.command(name="remove_reset",description="チャンネルログ削除の設定を削除するよ")
@commands.has_guild_permissions(manage_guild=True,manage_channels=True)
async def remove_reset(ctx):
    if not ctx.guild.id in guilds:
        await ctx.response.send_message("データが無いです")
        return
    guilds.pop(ctx.guild.id)
    await ctx.response.send_message("データを削除しました")

session.run(token)
