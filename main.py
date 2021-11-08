import os
from keep_alive import keep_alive
from discord.ext import commands
import discord

bot = commands.Bot(
  command_prefix="z?",  # Change to desired prefix
  case_insensitive=True,  # bot aren't case-sensitive
  help_command=None,
  intents=discord.Intents().all()
)


bot.author_id = 832264231617167381  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    await bot.change_presence( activity=discord.Game("Why leaderboard don't work?"))

@bot.command(name='sd')
async def sd(ctx):
  if ctx.author.id == bot.author_id:
    await bot.close()

my_secret = os.environ['token']
if __name__ == '__main__':  # Ensures this is the file being ran
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()  # Starts a webserver to be pinged.
token = os.environ['token']
bot.run(token)  # Starts the bot