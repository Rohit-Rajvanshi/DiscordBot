from discord.ext import commands
from discord import app_commands
import discord

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="add")
    async def add(self, interaction: discord.Interaction, arg1: int, arg2: int):
        result = arg1 + arg2
        await interaction.response.send_message(result)

    @app_commands.command(name="sub")
    async def sub(self, interaction: discord.Interaction, arg1: int, arg2: int):
        result = arg1 - arg2
        await interaction.response.send_message(result)

    @app_commands.command(name="multiply")
    async def multiply(self, interaction: discord.Interaction, arg1: int, arg2: int):
        result = arg1 * arg2
        await interaction.response.send_message(result)

    @app_commands.command(name="divide")
    async def divide(self, interaction: discord.Interaction, arg1: int, arg2: int):
        if arg2 == 0:
            await interaction.response.send_message("Cannot divide by zero ❌")
            return

        result = arg1 / arg2
        await interaction.response.send_message(result)


async def setup(bot):
    await bot.add_cog(Calculator(bot))