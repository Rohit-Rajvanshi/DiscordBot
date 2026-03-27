from discord.ext import commands
from discord import app_commands
import discord
import commands.variables as variables 
from datetime import timedelta


class Moderation(commands.Cog):

    def __init__(self , bot):
        self.bot = bot 

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self , ctx , user : discord.Member): 
        await user.ban()
        embed = discord.Embed(
            title = "Ban Successful",
            description = f"Banned **{user}** for being a VERY bad person!!",
            color = discord.Color.red(),
        )
        await ctx.reply(embed = embed)

    @ban.error
    async def ban_error(self ,ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self ,ctx , member : discord.Member):
        await member.kick()
        embed = discord.Embed(
            title = "Kick Successful",
            description = f"Kicked **{member}** for being a bad person!!",
            color = discord.Color.red(),
        )
        await ctx.reply(embed = embed)

    @kick.error
    async def kick_error(self ,ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)





    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self , ctx , user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        embed = discord.Embed(
            title = "Unban Successful",
            description = f"Unbanned **{user}** for being apologetic!!",
            color = discord.Color.orange(),
        )
        await ctx.reply(embed = embed)

    @unban.error
    async def unban_error(self ,ctx , error):
        if isinstance(error , commands.CommandInvokeError):
            embed = discord.Embed(
                title = "The user is not banned",
                description = "Revisit your Ban list",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)
        elif isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)


    @commands.command()
    @commands.has_permissions(moderate_members = True)
    async def mute(self ,ctx , member : discord.Member , hours : int , reason : str = None):
        duration = timedelta(hours = hours)
        if reason is None:
            reason = "No reason provided!"
        await member.timeout(duration , reason = reason)
        embed = discord.Embed(
            title = "Timed out",
            description = f"{member} has been successfuly timedout for {duration} hours",
            color = discord.Color.red()
        )
        await ctx.reply(embed = embed)

    @mute.error 
    async def mute_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self , ctx ,member : discord.Member):
        await member.edit(timed_out_until = None)
        embed = discord.Embed(
            title = "Removed Timeout",
            description = f"{member} has been successfuly unmuted",
            color = discord.Color.orange()
        )
        await ctx.reply(embed = embed)

    @unmute.error 
    async def unmute_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)


    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def censor(self ,ctx , method : str , *args):
        args_list = list(args)
        if method == "add":
            variables.Censor_list.extend(args_list)
            embed = discord.Embed(
                description = f"added **{args_list}** to the censor list",
                color = discord.Color.blue()
            )
            await ctx.reply(embed = embed)
        

        elif method == "remove":
            for arg in args_list:
                variables.Censor_list.remove(arg)
            embed = discord.Embed(
                description = f"removed **{args_list}** from the censor list",
                color = discord.Color.blue()
            )
            await ctx.reply(embed = embed)
        
        
        elif method == "clear":
            variables.Censor_list = []
            await ctx.reply(f"**CLEARED THE CENSOR LIST**")
        
        
        elif method == "list":
            description_string = ""
            for word in variables.Censor_list:
                description_string += f"-> {word}\n"
            embed = discord.Embed(
                title = "CENSOR LIST",
                description = description_string,
                color = discord.Color.blue()
            )
            await ctx.reply(embed = embed)
        
        else:
            await ctx.reply("**Invalid Syntax**")

    @censor.error 
    async def censor_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if message.author.guild_permissions.manage_members:
            await self.bot.process_commands(message)
            return

        for msg in message.content.split():
            if msg.lower() in variables.Censor_list:
                await message.delete()
                await message.channel.send(
                    f"Hey {message.author.mention} don't use that word!!!"
                )
                return

        await self.bot.process_commands(message)
    
async def setup(bot):
    await bot.add_cog(Moderation(bot))
        