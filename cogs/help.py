from discord.ext import commands
from discord import Embed

class HelpCommands(commands.Cog, name='Help Commands'):
    '''These are the fun commands'''
    def __init__(self, bot):
      self.bot = bot
    
    @commands.command(name='help',description='We know what is it.')
    async def help(self,ctx,*,command_for_help:str=None):
      embed = Embed(color=0x6ba4ff)
      embed.set_thumbnail(url=ctx.author.avatar_url)
      if command_for_help is None:
        cogs = self.bot.cogs
        for x in cogs:
          if x == 'Developer Commands':
            continue
          e = self.bot.get_cog(x)
          wit = e.get_commands()
          w = ''
          for y in wit:
            w += f'`{y.name}` {y.description}\n'
          if w == '':
            pass
          else:
            embed.add_field(name=x,value=f'{w} \n', inline=False)
      else:
        wit = self.bot.get_command(command_for_help)
        if wit is not None:
          s = ''
          if wit.description == '':
            s = 'None for now'
            embed.add_field(name=wit.name,value=s)
          else:
            embed.add_field(name=wit.name,value=wit.description)
        else:
            embed.add_field(name='No command found!',value='404 Not Found')
      await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(HelpCommands(bot))

#"https://cdn.discordapp.com/attachments/900186121655435314/902883906263601202/Untitled_-_Copy.png"