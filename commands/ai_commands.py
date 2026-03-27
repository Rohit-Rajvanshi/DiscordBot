from ai import KuroAI
from discord.ext import commands
from discord import app_commands
import discord
import os 
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
ai = KuroAI(API_KEY)



class AI_COMMANDS(commands.Cog):

    def __init__(self , bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.has_permissions(administrator = True)
    async def ask(self , interaction : discord.Interaction , question :str):
        await interaction.response.defer()

        embed = await ai.ask(question)

        await interaction.followup.send(embed = embed)

    @ask.error 
    async def ask_error(self , interaction: discord.Interaction, error):
        await interaction.response.send_message(
            "**You don't have permission to use this.**",
            ephemeral=True
        )

    @app_commands.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def summarize(self , interaction : discord.Interaction , question :str):
        await interaction.response.defer()

        embed = await ai.ask(f"Summarize this:{question}")

        await interaction.followup.send(embed = embed)

    @summarize.error 
    async def summarize_error(self , interaction: discord.Interaction, error):
        await interaction.response.send_message(
            "**You don't have permission to use this.**",
            ephemeral=True
        )
        
async def setup(bot):
    await bot.add_cog(AI_COMMANDS(bot))