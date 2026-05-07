from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument: `{error.param.name}`\nUsage: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`")
        elif isinstance(error, commands.CommandNotFound):
            pass  # silently ignore
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Invalid argument. Usage: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`")
        else:
            await ctx.send(f"An error occurred: `{error}`")

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))