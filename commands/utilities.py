from discord.ext import commands
from discord import app_commands
import discord
import requests
from PIL import Image
from io import BytesIO
import random


class Utilities(commands.Cog):

    def __init__(self , bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self , member):
        await member.send(f"Hey {member.name} Welcome to the server")

    
    
    def to_upper(argument):
        return argument.upper()


    @commands.command()
    async def capitalize(self , ctx , * , content : to_upper):
        await ctx.reply(content)


    @commands.command()
    async def av(self ,ctx , member : discord.Member = None):
        if member is None:
            user = ctx.author
            await ctx.reply(user.avatar.url)
        else:
            await ctx.reply(member.avatar.url)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def role(self ,ctx , method : str , member : discord.Member , r : str):
        if method == "assign":
            for role in ctx.guild.roles:
                if role.name.lower() == r.lower():
                    await member.add_roles(role)
                    embed = discord.Embed(
                        description = f"{member.mention} has been assigned the role **{role}**",
                        color = discord.Color.pink()
                    )
                    await ctx.reply(embed = embed)
        elif method == "remove":
            for role in ctx.guild.roles:
                if role.name.lower() == r.lower():
                    await member.remove_roles(role)
                    embed = discord.Embed(
                        description = f"**{role}** role has been removed from {member.mention}",
                        color = discord.Color.pink()
                    )
                    await ctx.reply(embed = embed)

    @role.error
    async def role_error(self ,ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)
        else:
            await ctx.reply("Invalid syntax or role")

    @commands.command()
    async def gif(self , ctx):
        reference = ctx.message.reference
        if reference is None:
            await ctx.reply("Reply to the attachment")
            return 
        
        message_id = reference.message_id
        replied_message = await ctx.channel.fetch_message(message_id)

        if replied_message.attachments:
            attachment = replied_message.attachments[0]
            if attachment.content_type is None:
                return
            if attachment.content_type.startswith("image/"):
                url = attachment.url
                response = requests.get(url)

                img=Image.open(BytesIO(response.content))
                img = img.convert("RGB")
                img.save("convert.gif")

                await ctx.reply(file=discord.File("convert.gif"))
        else:
            await ctx.reply("No attachment found")
            return

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def setnick(self , ctx , member: discord.Member , *nickname):
        nick = " ".join(nickname)
        await member.edit(nick=nick)
        embed = discord.Embed(
            description = f"**{member}** has been assigned the nickname **{nick}**",
            color = discord.Color.purple()
        )
        await ctx.reply(embed = embed)


    @commands.command()
    async def cflip(self ,ctx):
        coin_possibilities = ["Heads" , "Tails"]
        output = random.choice(coin_possibilities)
        await ctx.reply(f"**The coin flipped and it landed on {output}**")


    @commands.command()
    async def count(self ,ctx):
        guild = ctx.guild
        count = len(ctx.guild.members)
        embed = discord.Embed(
            title = "Member Count",
            description = f"{count}",
            color = discord.Color.blue()
        )
        await ctx.reply(embed = embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lock(self ,ctx):
        channel = ctx.channel
        role = ctx.guild.default_role
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False

        await ctx.channel.set_permissions(role , overwrite=overwrite)

        await ctx.send("**🔒 Channel locked.**")


    @lock.error
    async def lock_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock(self ,ctx):
        channel = ctx.channel
        role = ctx.guild.default_role
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = True

        await ctx.channel.set_permissions(role , overwrite=overwrite)

        await ctx.send("**🔓 Channel unlocked.**")

    @unlock.error
    async def unlock_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)

    
    @commands.command()
    async def poll(self ,ctx , * , question):
        embed = discord.Embed(title ="New Poll" , description = question , color = discord.Color.blue())
        poll_message = await ctx.send(embed = embed)
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self , ctx , number : int):
        channel = ctx.channel
        await channel.purge(limit = number)

        embed = discord.Embed(description = f"Successfuly purged {number} messages")
        await ctx.send(embed = embed)


    @purge.error
    async def purge_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def banlist(self , ctx):
        ban_string = ""
        async for ban in ctx.guild.bans():
            ban_string += f"-> {ban.user}\n"
        embed = discord.Embed(
            title = "Ban List",
            description = ban_string,
            color = discord.Color.blue()
        )
        await ctx.send(embed = embed)

    @banlist.error
    async def banlist_error(self ,ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self , ctx , duration: int):
        await ctx.channel.edit(slowmode_delay = duration)
        await ctx.send(f"**Slowmode set to {duration} seconds!!**")

    @slowmode.error
    async def slowmode_error(ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "BUDDY BUDDY 😂😂😂",
                color = discord.Color.yellow(),
            )
            await ctx.reply(embed = embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))
        