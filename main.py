import discord
from discord.ext import commands,tasks
import datetime
import pytz

session = discord.Client(intents=discord.Intents.all())
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
    for guildjson in guilds:
      guilddata=guilds[guildjson]
      guild=guild = session.get_guild(guilddata["id"])
      for channel in guild.text_channels:
        if channel.topic==None:continue
        if 'channelresetter' in channel.topic:
          position = channel.position
          await channel.delete()
          resetedchannel = await channel.clone()
          await resetedchannel.edit(position=position)
          embed = discord.Embed(title='チャンネルをリセットしました',description='サポートアカウント:[@whitehatpy](https://twitter.com/whitehatpy', timestamp=datetime.datetime.utcnow())
          embed.set_footer(text=f"Produced by @whitehatpy", icon_url=client.user.avatar_url)
          await resetedchannel.send(embed=embed)
