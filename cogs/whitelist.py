from discord.ext import commands
import discord
from replit import db

class Whitelist(commands.Cog, name='Whitelist'):
  def __init__(self,bot):
    self.bot = bot

  @commands.command(name='Whitelist',description='Make commands useable in a channel',aliases=['wl'])
  @commands.has_permissions(manage_channels=True)
  async def wl (self,ctx,channel:discord.TextChannel=None):
    if channel is not None:
      channels = []
      try:
        channels = db["channels"]
      except:
        pass
      channels.append(channel.id)
    else:
      channels = []
      try:
        channels = db["channels"]
      except:
        pass
      channels.append(ctx.channel.id)
    db["channels"] = channels
    await ctx.send('Done')

def setup(bot):
  bot.add_cog(Whitelist(bot))