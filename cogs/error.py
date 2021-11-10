from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, CommandNotFound, NotOwner, MissingRequiredArgument, TooManyArguments, BotMissingPermissions,MaxConcurrencyReached,CommandOnCooldown

class OnCommandErrorCog(commands.Cog, name="on command error"):
  def __init__(self, bot:commands.Bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_command_error(self, ctx:commands.Context, error:commands.CommandError):
    if isinstance(error, MaxConcurrencyReached):
      pass
    if isinstance(error, CommandOnCooldown):
      day = round(error.retry_after/86400)
      hour = round(error.retry_after/3600)
      minute = round(error.retry_after/60)
      if day > 0:
        await ctx.send('This command has a cooldown, for '+str(day)+ "day(s)")
      elif hour > 0:
        await ctx.send('This command has a cooldown, for '+str(hour)+ " hour(s)")
      elif minute > 0:
        await ctx.send('This command has a cooldown, for '+ str(minute)+" minute(s)")
      else:
        await ctx.send(f'This command has a cooldown, for {error.retry_after:.2f} second(s)')
    elif isinstance(error, CommandNotFound):
      await ctx.send("No command found",delete_after=3)
    elif isinstance(error, MissingPermissions):
      await ctx.send("❌ You don't have permission to do that.",delete_after=3.0)
    elif isinstance(error, BotMissingPermissions):
      await ctx.send("I don't have permission to do that :(",delete_after=3.0)
    elif isinstance(error, CheckFailure):
      await ctx.send(error)
    elif isinstance(error, NotOwner):
      await ctx.send(error)
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send("A argument is missing",delete_after=3.0)
    elif isinstance(error, TooManyArguments):
        await ctx.send("Some arguments are more than needed.",delete_after=3.0)
    else:
      print(error)
      await ctx.send('error',delete_after=3.0)
 
def setup(bot):
	bot.add_cog(OnCommandErrorCog(bot))