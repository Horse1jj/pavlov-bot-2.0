import discord
from discord.ext import commands
from utils.discord_embeds import status_embed

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = status_embed(
                "Missing argument",
                f"`{error.param.name}` is required.\nUsage: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`",
                success=False
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=status_embed(
                "Unknown command",
                f"Use `{ctx.prefix}help` to see available commands.",
                success=False
            ))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=status_embed(
                "Invalid argument",
                f"Usage: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`",
                success=False
            ))
        else:
            await ctx.send(embed=status_embed(
                "Command error",
                f"An error occurred: `{error}`",
                success=False
            ))

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
