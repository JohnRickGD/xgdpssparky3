import os
from keep_alive import keep_alive
from discord.ext import commands
import random
import json
import discord
import asyncio

bot = commands.Bot(
  command_prefix="se?",  # Change to desired prefix
  case_insensitive=True  # bot aren't case-sensitive
)

bot.author_id = 487258918465306634  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

def getCash(ctx):
  with open('stats.json')as f:
    stats = f.read()
    print(stats)
    json.loads(stats)
    return stats[f'{ctx.author.id}']

def setCash(ctx,value):
  stats={}
  with open('stats.json','r')as f:
    stats = json.loads(f.read())
    print(stats)
  with open('stats.json','w')as f:
    stats.update({f'{ctx.author.id}' : value})
    print(stats)
    f.write(json.dumps(stats))

@bot.command(name='cash')
async def cash(ctx):
  try:
    await ctx.send(f'You are having {getCash(ctx=ctx)} CPs')
  except KeyError:
    await ctx.send(f'You are having 0 CPs')

@bot.command(name='guess',aliases=['g'])
async def guess(ctx,difficult=None):
    if difficult is None:
      difficult = random.choice(['easy','medium','hard'])
    difficult = difficult.lower()
    with open('cogs/level.json')as f:
      levels = json.loads(f.read())
      levels = levels['difficult'][difficult]
      difficultColor = 0
      if difficult.lower() == 'easy':
        difficultColor = 0x29ff30
      elif difficult.lower() == 'medium':
        difficultColor == 0xfbff29
      elif difficult.lower() == 'hard':
        difficultColor == 0xff643d
      levelName = random.choice(list(levels.keys()))
      embed = discord.Embed(title='Guess the level',description=f'Difficult: {difficult}', color=difficultColor)
      embed.set_image(url=levels[levelName])
      await ctx.send(embed=embed)
      def check(m):
        return m.content == levelName.lower() and m.channel == ctx.message.channel
      try:
        try:
          value = getCash(ctx=ctx)
        except:
          setCash(ctx=ctx,value=0)
          value = 0
        await ctx.bot.wait_for('message', check=check,timeout=12.0)
        if difficult.lower() == 'easy':
            amount = random.randint(1, 20)
            value += amount
        if difficult.lower() == 'medium':
            amount = random.randint(21,40)
            value += amount
        if difficult.lower() == 'hard':
            amount = random.randint(41, 60)
            value += amount
        setCash(ctx=ctx,value=value)
        embed = discord.Embed(title=f'Congratulation, you guessed {levelName} correctly!',description=f'You have been awarded {amount} Creator Points, {ctx.author.mention}')
        await ctx.send(embed=embed)
      except asyncio.TimeoutError:
        embed = discord.Embed(title=f'Time out!',color=difficultColor)
        await ctx.send(embed=embed)

my_secret = os.environ['token']
if __name__ == '__main__':  # Ensures this is the file being ran
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()  # Starts a webserver to be pinged.
token = os.environ['token']
bot.run(token)  # Starts the bot