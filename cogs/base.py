import os
from discord.ext import commands
import json
import discord
import random
import asyncio
from disrank2.generator import Generator #upm package(Disrank2)

def getCash(ctx):
  with open('cogs/stats.json')as f:
    stats = f.read()
    stats = json.loads(stats)
    return stats[f'{ctx.id}']["CP"]

def setCash(ctx,value):
  stats={}
  with open('cogs/stats.json','r')as f:
    stats = json.loads(f.read())
  with open('cogs/stats.json','w')as f:
    stats.update({f'{ctx.id}' : {"CP":value}})
    f.write(json.dumps(stats))


class MainCommands(commands.Cog, name='Main Commands'):
    def __init__(self, bot):
      self.bot = bot

    @commands.cooldown(rate=1,per=60*60*24)
    @commands.command(name='daily')
    async def daily(self,ctx):
      cp =getCash(ctx=ctx.author)
      setCash(ctx=ctx.author,value=cp+25)
      embed = discord.Embed(title='Claimed',description='You got 25 CPs',color=0x7aadff)
      await ctx.send(embed=embed)

    @commands.command(name='credit')
    async def credit(self,ctx):
      embed = discord.Embed(title='Credits',description='Bot: `Brain Flooder#9985`\nImage: `ZumidoGD#5369`\nPrepared by ZumidoGD',color=0x7aadff)
      await ctx.send(embed=embed)

    @commands.command(name='profile',aliases=['p'])
    async def profile(self,ctx):
      args = {
      'bg_image' : 'https://cdn.discordapp.com/attachments/907840531101544508/907888368468242463/Selected_bannger.png', # Background image link {}
      'profile_image' : f'{ctx.author.avatar_url}', # User profile picture link
      'next_xp' : 30000000, #TeamSeas
      'user_xp' : getCash(ctx.author), # User current xp
      'user_name' : f'{ctx.author.name}#{ctx.author.discriminator}', # user name with descriminator 
      'text_color' : '#ffffff', # Text color un HEX
  }
      image = Generator().generate_profile(**args)

      # In a discord command
      file = discord.File(fp=image, filename='image.png')
      await ctx.send(file=file)

    @commands.max_concurrency( number=1,wait = False )
    @commands.command(name='guess',aliases=['g'])
    async def guess(self,ctx,difficult=None):
        if difficult is None:
          difficult = random.choice(['easy','medium','hard'])
        difficult = difficult.lower()
        with open('cogs/level.json')as f:
          levels = json.loads(f.read())
          levels = levels['difficult'][difficult]
          if difficult.lower() == 'easy':
            difficultColor = discord.Colour.green()
          elif difficult.lower() == 'medium':
            difficultColor = discord.Colour.orange()
          elif difficult.lower() == 'hard':
            difficultColor = discord.Colour.red()
          levelName = random.choice(list(levels.keys()))
          embed = discord.Embed(title='Guess the level',description=f'Difficult: {difficult}', color=difficultColor)
          embed.set_image(url=levels[levelName])
          embed.set_footer(text=f'Requested by {ctx.author.name}{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
          def check(m):
            return m.content.lower() == levelName.lower() and m.channel == ctx.message.channel and m
          try:
            try:
              value = getCash(ctx.author)
            except:
              setCash(ctx.author,value=0)
              value = 0
            msg = await ctx.bot.wait_for('message', check=check,timeout=20.0)
            if difficult.lower() == 'easy':
                amount = random.randint(1, 20)
                value += amount
            if difficult.lower() == 'medium':
                amount = random.randint(21,40)
                value += amount
            if difficult.lower() == 'hard':
                amount = random.randint(41, 60)
                value += amount
            setCash(msg.author,value=value)
            embed = discord.Embed(title=f'Congratulations!, You guessed {levelName} correctly!',description=f'You have been awarded {amount} Creator Points, {msg.author.mention}',color=0xffffff)
            await ctx.send(embed=embed)
          except asyncio.TimeoutError:
            embed = discord.Embed(title=f'Time\'s up!',color=0xffffff)
            await ctx.send(embed=embed)
    
    @commands.command(name='leaderboard',aliases=['lb'],description='Show the top 20 richest users')
    async def lb(self,ctx):
        e = {}
        high = {}
        for x in ctx.guild.members:
          try:
            e.update({x.name:getCash(x)})
          except KeyError:
            e.update({x.name: 0})
        high=dict(sorted(e.items(),key= lambda x:x[1], reverse = True))
        text = ''
        e = 0
        for x in high:
          if e == 20:
            return
          else:
            text += f'{x}: {high[x]}\n'
          e+=1
        embed = discord.Embed(title=f'Top highest in {ctx.guild.name}',description=text,color=0x6ba4ff)
        await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(MainCommands(bot))
my_secret = os.environ['token']