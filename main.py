import discord
from discord.ext import commands,tasks
import datetime
import pytz

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
@tasks.loop(seconds=5)
async def nuke_channels():
    nowtime = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
    if nowtime in resettimes:
    for guildid in guilds:
      guild = session.get_guild(int(guildid))
      for channel in guild.text_channels:
        if channel.topic==None:continue
        if 'channelresetter' in channel.topic:
          position = channel.position
          await channel.delete()
          resetedchannel = await channel.clone()
          await resetedchannel.edit(position=position)
          embed = discord.Embed(title='チャンネルをリセットしました',description='サポートアカウント:[@whitehatpy](https://twitter.com/whitehatpy', timestamp=datetime.datetime.utcnow())
          embed.set_footer(text=f"Produced by @whitehatpy", icon_url=session.user.avatar_url)
          await resetedchannel.send(embed=embed)

@session.slash_command(name="setupnuke",description="チャンネルログ削除を設定するよ")
@commands.has_guild_permissions(manage_guild=True,manage_channels=True)
async def setupnuke(ctx):
  if ctx.guild.id in guilds:
    await ctx.respond("設定しています")
    return
  guilds[ctx.guild.id]={}
  await ctx.respond("設定しました")

@session.slash_command(name="unsetupnuke",description="チャンネルログ削除の設定を削除するよ")
@commands.has_guild_permissions(manage_guild=True,manage_channels=True)
async def unsetupnuke(ctx):
  if　not ctx.guild.id in guilds:
    await ctx.respond("データが無いです")
    return
  guilds.pop(ctx.guild.id)
  await ctx.respond("データを削除しました")
session.run(token)
