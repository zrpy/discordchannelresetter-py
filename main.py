import discord
from discord.ext import commands,tasks
import datetime
import pytz
import asyncio

session = discord.Client(intents=discord.Intents.all())
token=""
guilds={}
resettimes={
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
                time_list=re.findall(r'reset_time\[(\d+:\d+),(\d+:\d+)\]', channel.topic)
                if len(times)==0:
                    times=resettimes
                else:
                    times=time_list[0]
                now = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
                if now in times:
                    position = channel.position
                    await channel.delete()
                    resetedchannel = await channel.clone()
                    await resetedchannel.edit(position=position)
                    embed = discord.Embed(title='チャンネルをリセットしました',description='サポートアカウント:[@whitehatpy](https://twitter.com/whitehatpy)', timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"Produced by @whitehatpy", icon_url=session.user.avatar_url)
                    await resetedchannel.send(embed=embed)

@tasks.loop(seconds=20)
async def nukeloops():
    tasks=[]
    for guildid in guilds:
        tasks.append(asyncio.create_task(nuker(guildid)))
    await asyncio.gather(*tasks)

@session.event
async def on_ready():
    nukeloops.start()

@session.slash_command(name="add_reset",description="チャンネルログ削除を設定するよ")
@commands.has_guild_permissions(manage_guild=True,manage_channels=True)
async def add_reset(ctx):
    if ctx.guild.id in guilds:
        await ctx.respond("設定しています")
        return
    guilds[ctx.guild.id]={}
    await ctx.respond("設定しました")

@session.slash_command(name="remove_reset",description="チャンネルログ削除の設定を削除するよ")
@commands.has_guild_permissions(manage_guild=True,manage_channels=True)
async def remove_reset(ctx):
    if not ctx.guild.id in guilds:
        await ctx.respond("データが無いです")
        return
    guilds.pop(ctx.guild.id)
    await ctx.respond("データを削除しました")

session.run(token)
