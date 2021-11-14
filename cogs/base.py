from discord.ext import commands
import json
import discord
import random
import asyncio
from replit import db
from disrank2.generator import Generator #upm package(Disrank2)

def getCash(ctx):
  try:
    value = db[f"{ctx.id}"]
    return int(value)
  except KeyError:
    db[f"{ctx.id}"] = "0"
    return 0

def setCash(ctx,value):
  db[f"{ctx.id}"] = f"{value}"

def checkIsWhite(channel):
  try:
    channels = db["channels"]
    if channel.id in channels:
      return True
    else:
      return False
  except:
    db["channels"] = []
    return False

def getWhitelisted():
  try:
    channels = db["channels"]
    return channels
  except KeyError:
    db["channel"] = []
    return []


class MainCommands(commands.Cog, name='Main Commands'):
    def __init__(self, bot):
      self.bot = bot
      
    @commands.command(name='gdps')
    async def gdps(self,ctx):
      embed=discord.Embed(title='XGDPS Download and Server', description='So you want to play XGDPS? You are lucky because we have collected some links for it.',color=0x6ba4ff)
      embed.add_field(name='XGDPS Official Server', value='[Click me](https://discord.gg/xM6CKY9u)', inline=False)
      embed.add_field(name='Glubfub Official support server', value='[Click me](https://discord.gg/XkEXfakk4M)', inline=False)
      embed.add_field(name='PC [.rar]', value='[Click me](http://xcggdpsserver.xyz/XGDPS.rar)', inline=False)
      embed.add_field(name='PC [.zip]', value='[Click me](http://xcggdpsserver.xyz/XGDPS.zip)', inline=False)
      embed.add_field(name='Mobile [Android only]', value='[Click me](http://xcggdpsserver.xyz/XGDPS.apk)', inline=False)
      embed.set_footer(text='Note: NET-Framework and Visual C++ Redistributable packets are needed for PC version.')
      await ctx.send(embed=embed)
    @commands.command(name='levels')
    async def lvls(self,ctx):
      if checkIsWhite(ctx.channel) == False:
          print(getWhitelisted())
          return
      with open('cogs/level.json')as f:
        levels = json.loads(f.read())
        e=0
        for x in levels["difficulty"]:
          for y in levels["difficulty"][x]:
            e+=1
      await ctx.send(e)

    @commands.command(name='gift')
    async def gift(self,ctx,user:discord.Member,value:int):
      if checkIsWhite(ctx.channel) == False:
          print(getWhitelisted())
          return
      if user == ctx.author:
        embed=discord.Embed(title="Fixed bug", description="You have found a fixed bug!", color=0x66bdff)
        await ctx.send(embed=embed)
        return
      user1 = getCash(ctx=ctx.author)
      if user1 < value:
        embed=discord.Embed(title='You dont have enough Creator Points!',color=0x7aadff)
        await ctx.send(embed=embed)
        return
      if value <= 0:
        await ctx.send('User used hack. We have fixed it before.')
      user2 = getCash(ctx=user)
      user1 -= value
      setCash(ctx = ctx.author,value = user1)
      user2 += value
      setCash(ctx = user,value = user2)
      embed = discord.Embed(title='Done!',description=f'{ctx.author.mention} has gifted {user.mention} {value} Creator Points!',color=0x7aadff)
      await ctx.send(embed=embed)

    @commands.cooldown(1,60*60*24,commands.BucketType.member)
    @commands.command(name='daily')
    async def daily(self,ctx):
      cp =getCash(ctx=ctx.author)
      cp+=25
      setCash(ctx=ctx.author,value=cp)
      embed = discord.Embed(title='You claimed your daily reward!',description='You earned 25 Creator Points!',color=0x7aadff)
      await ctx.send(embed=embed)

    @commands.command(name='credits')
    async def credit(self,ctx):
      if checkIsWhite(ctx.channel) == False:
          print(getWhitelisted())
          return
      embed = discord.Embed(title='Credits',description='**Bots Code:**\nBrain Flooder#9985\n**Image: \n**ZumidoGD#5369\nMegumin b#9045\nTPD9#0009\n**Bot Developer:** \nTicLos#4246',color=0x7aadff)
      await ctx.send(embed=embed)

    @commands.command(name='profile',aliases=['p'])
    async def profile(self,ctx,member:discord.Member=None):
      if checkIsWhite(ctx.channel) == False:
          print(getWhitelisted())
          return
      if member is None:
        user = ctx.author
      else:
        user = member
      args = {
      'bg_image' : 'https://cdn.discordapp.com/attachments/907601472450093136/907988510068342864/530_sin_titulo_20211110144152.png', # Background image link {}
      'profile_image' : f'{user.avatar_url}', # User profile picture link
      'next_xp' : 30000000, #TeamSeas
      'user_xp' : getCash(user), # User current xp
      'user_name' : f'{user.name}#{user.discriminator}', # user name with descriminator 
      'text_color' : '#ffffff', # Text color un HEX
  }
      image = Generator().generate_profile(**args)

      # In a discord command
      file = discord.File(fp=image, filename='image.png')
      await ctx.send(file=file)

    @commands.max_concurrency(number = 1, per = commands.BucketType.channel, wait = False )
    @commands.command(name='guess',aliases=['g'])
    async def guess(self,ctx,difficulty=None):
        if checkIsWhite(ctx.channel) == False:
          print(getWhitelisted())
          return
        difficultyRank = ['easy','medium','hard']
        if difficulty is not None:
          if difficulty not in difficultyRank:
            difficulty = random.randint(0,1000)
            if difficulty == 0:
              difficulty = 'legendary'
            else:
              difficulty = random.choice(['easy','medium','hard'])
        if difficulty is None:
          difficulty = random.randint(0,500)
          if difficulty == 0:
            difficulty = 'legendary'
          else:
            difficulty = random.choice(['easy','medium','hard'])
        difficulty = difficulty.lower()
        with open('cogs/level.json')as f:
          levels = json.loads(f.read())
          levels = levels['difficulty'][difficulty]
          if difficulty.lower() == 'easy':
            difficultyColor = discord.Colour.green()
          elif difficulty.lower() == 'medium':
            difficultyColor = discord.Colour.orange()
          elif difficulty.lower() == 'hard':
            difficultyColor = discord.Colour.red()
          else:
            difficultyColor = discord.Colour.purple()
          levelName = random.choice(list(levels.keys()))
          embed = discord.Embed(title='Guess the level',description=f'Difficulty: {difficulty}', color=difficultyColor)
          embed.set_image(url=levels[levelName])
          embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
          yam = await ctx.send(embed=embed)
          def check(m):
            return m.content.lower() == levelName.lower() and m.channel == ctx.message.channel and m
          try:
            msg = await ctx.bot.wait_for('message', check=check,timeout=20.0)
            try:
              value = getCash(msg.author)
            except:
              setCash(msg.author,value=0)
              value = 0
            if difficulty.lower() == 'easy':
                amount = random.randint(1, 20)
                value += amount
            elif difficulty.lower() == 'medium':
                amount = random.randint(21,40)
                value += amount
            elif difficulty.lower() == 'hard':
                amount = random.randint(41, 60)
                value += amount
            else:
              amount = random.randint(80,100)
              value += amount
            setCash(msg.author,value=value)
            embed = discord.Embed(title=f'Congratulations!, You guessed {levelName} correctly!',description=f'You have been awarded {amount} Creator Points, {msg.author.mention}',color=0xffffff)
            if difficulty == 'legendary':
              await ctx.send(embed=embed,delete_after=3.0)
              await asyncio.sleep(3.0)
              await msg.delete()
              await yam.delete()
            else:
              await ctx.send(embed=embed)
          except asyncio.TimeoutError:
            embed = discord.Embed(title=f'Time\'s up!',color=0xffffff)
            await ctx.send(embed=embed)
    
    @commands.command(name='topcp')
    async def lb(self,ctx):
        e = {}
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
            break
          else:
            text += f'{x}: {high[x]}\n'
          e+=1
        embed = discord.Embed(title=f'Top highest in {ctx.guild.name}',description=text,color=0x6ba4ff)
        await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(MainCommands(bot))