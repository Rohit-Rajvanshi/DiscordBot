import discord 
from discord.ext import commands 
import os 
from dotenv import load_dotenv
from discord import app_commands
import asyncio

load_dotenv()

description = "Kuro , a multifunctional Discord bot with moderation , role management , fun utilities and AI integration"

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True 

Skoll = commands.Bot(command_prefix = "?" , description=description , intents=intents , case_insensitive = True)

@Skoll.event 
async def on_ready():

    assert Skoll.user is not None
    print (f"Logged in as {Skoll.user} (ID : {Skoll.user.id})")
    print("---------------------------------------------------")
    guild = discord.Object(id = 1104576336690937928)
    await Skoll.tree.sync(guild=guild)
    print("CLEARED + SYNCED")
async def main():
    async with Skoll:
        await Skoll.load_extension("commands.moderation")
        await Skoll.load_extension("commands.calculator")
        await Skoll.load_extension("commands.ai_commands")
        await Skoll.load_extension("commands.utilities")
        await Skoll.load_extension("ttt.game")
        await Skoll.start(TOKEN)

asyncio.run(main())

                                                                                                                   
