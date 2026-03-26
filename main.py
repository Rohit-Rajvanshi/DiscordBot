import discord 
from discord.ext import commands 
import random 
import os 
from dotenv import load_dotenv
from datetime import timedelta
import variables
import requests
from PIL import Image
from io import BytesIO
import random 

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

@Skoll.event
async def on_message(message):
    if message.author == Skoll.user:
        return 
    if message.author.guild_permissions.manage_messages:
        await Skoll.process_commands(message);
        return 

    for msg in message.content.split():
        if msg.lower() in variables.Censor_list:
            await message.delete()
            await message.channel.send(f"Hey {message.author.mention} dont use that word!!!")
            return 

    await Skoll.process_commands(message);

@Skoll.event
async def on_member_join(member):
    await member.send(f"Hey {member.name} welcome to the server")

def to_upper(argument):
    return argument.upper()


@Skoll.command()
async def capitalize(ctx , * , content : to_upper):
    await ctx.reply(content)


@Skoll.command()
async def av(ctx , member : discord.Member = None):
    if member is None:
        user = ctx.author
        await ctx.reply(user.avatar.url)
    else:
        await ctx.reply(member.avatar.url)

@Skoll.command()
@commands.has_permissions(administrator=True)
async def ban(ctx , user : discord.Member): 
    await user.ban()
    embed = discord.Embed(
        title = "Ban Successful",
        description = f"Banned **{user}** for being a VERY bad person!!",
        color = discord.Color.red(),
    )
    await ctx.reply(embed = embed)

@ban.error
async def ban_error(ctx , error):
    if isinstance(error , commands.MissingPermissions):
        embed = discord.Embed(
            title = "Missing Permissions",
            description = "BUDDY BUDDY 😂😂😂",
            color = discord.Color.yellow(),
        )
        await ctx.reply(embed = embed)



@Skoll.command()
@commands.has_permissions(administrator=True)
async def kick(ctx , member : discord.Member):
    await member.kick()
    embed = discord.Embed(
        title = "Kick Successful",
        description = f"Kicked **{member}** for being a bad person!!",
        color = discord.Color.red(),
    )
    await ctx.reply(embed = embed)

@kick.error
async def kick_error(ctx , error):
    if isinstance(error , commands.MissingPermissions):
        embed = discord.Embed(
            title = "Missing Permissions",
            description = "BUDDY BUDDY 😂😂😂",
            color = discord.Color.yellow(),
        )
        await ctx.reply(embed = embed)





@Skoll.command()
@commands.has_permissions(administrator=True)
async def unban(ctx , user_id: int):
    user = await Skoll.fetch_user(user_id)
    await ctx.guild.unban(user)
    embed = discord.Embed(
        title = "Unban Successful",
        description = f"Unbanned **{user}** for being apologetic!!",
        color = discord.Color.orange(),
    )
    await ctx.reply(embed = embed)

@unban.error
async def unban_error(ctx , error):
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


@Skoll.command()
@commands.has_permissions(moderate_members = True)
async def mute(ctx , member : discord.Member , hours : int , reason : str = None):
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
async def mute_error(ctx , error):
    if isinstance(error , commands.MissingPermissions):
        embed = discord.Embed(
            title = "Missing Permissions",
            description = "BUDDY BUDDY 😂😂😂",
            color = discord.Color.yellow(),
        )
        await ctx.reply(embed = embed)

@Skoll.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx ,member : discord.Member):
    await member.edit(timed_out_until = None)
    embed = discord.Embed(
        title = "Removed Timeout",
        description = f"{member} has been successfuly unmuted",
        color = discord.Color.orange()
    )
    await ctx.reply(embed = embed)

@unmute.error 
async def unmute_error(ctx , error):
    if isinstance(error , commands.MissingPermissions):
        embed = discord.Embed(
            title = "Missing Permissions",
            description = "BUDDY BUDDY 😂😂😂",
            color = discord.Color.yellow(),
        )
        await ctx.reply(embed = embed)


@Skoll.command()
@commands.has_permissions(moderate_members=True)
async def censor(ctx , method : str , *args):
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



@Skoll.command()
@commands.has_permissions(administrator = True)
async def role(ctx , method : str , member : discord.Member , r : str):
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
async def role_error(ctx , error):
    if isinstance(error , commands.MissingPermissions):
        embed = discord.Embed(
            title = "Missing Permissions",
            description = "BUDDY BUDDY 😂😂😂",
            color = discord.Color.yellow(),
        )
        await ctx.reply(embed = embed)
    else:
        await ctx.reply("Invalid syntax or role")

@Skoll.command()
async def gif(ctx):
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

@Skoll.command()
@commands.has_permissions(moderate_members=True)
async def setnick(ctx , member: discord.Member , *nickname):
    nick = " ".join(nickname)
    await member.edit(nick=nick)
    embed = discord.Embed(
        description = f"**{member}** has been assigned the nickname **{nick}**",
        color = discord.Color.purple()
    )
    await ctx.reply(embed = embed)


@Skoll.command()
async def cflip(ctx):
    coin_possibilities = ["Heads" , "Tails"]
    output = random.choice(coin_possibilities)
    await ctx.reply(f"**The coin flipped and it landed on {output}**")


@Skoll.command()
async def count(ctx):
    guild = ctx.guild
    count = len(ctx.guild.members)
    embed = discord.Embed(
        title = "Member Count",
        description = f"{count}",
        color = discord.Color.blue()
    )
    await ctx.reply(embed = embed)

@Skoll.command()
@commands.has_permissions(administrator=True)
async def lock(ctx):
    channel = ctx.channel
    role = ctx.guild.default_role
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = False

    await ctx.channel.set_permissions(role , overwrite=overwrite)

    await ctx.send("**🔒 Channel locked.**")


@lock.error
async def lock_error(ctx , error):
    if isinstance(error , commands.MissingPermissions):
        embed = discord.Embed(
            title = "Missing Permissions",
            description = "BUDDY BUDDY 😂😂😂",
            color = discord.Color.yellow(),
        )
        await ctx.reply(embed = embed)

@Skoll.command()
@commands.has_permissions(administrator=True)
async def unlock(ctx):
    channel = ctx.channel
    role = ctx.guild.default_role
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = True

    await ctx.channel.set_permissions(role , overwrite=overwrite)

    await ctx.send("**🔓 Channel unlocked.**")

@unlock.error
async def unlock_error(ctx , error):
    if isinstance(error , commands.MissingPermissions):
        embed = discord.Embed(
            title = "Missing Permissions",
            description = "BUDDY BUDDY 😂😂😂",
            color = discord.Color.yellow(),
        )
        await ctx.reply(embed = embed)

  
@Skoll.command()
async def poll(ctx , * , question):
    embed = discord.Embed(title ="New Poll" , description = question , color = discord.Color.blue())
    poll_message = await ctx.send(embed = embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@Skoll.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx , number : int):
    channel = ctx.channel
    await channel.purge(limit = number)

    embed = discord.Embed(description = f"Successfuly purged {number} messages")
    await ctx.send(embed = embed)


@purge.error
async def purge_error(ctx , error):
    if isinstance(error , commands.MissingPermissions):
        embed = discord.Embed(
            title = "Missing Permissions",
            description = "BUDDY BUDDY 😂😂😂",
            color = discord.Color.yellow(),
        )
        await ctx.reply(embed = embed)



@Skoll.command()
async def add(ctx , arg1 : int  ,arg2 : int):
    sum = arg1 + arg2
    await ctx.reply(sum)

@Skoll.command()
async def sub(ctx , arg1 :int , arg2 :int ):
    result = arg1 - arg2
    await ctx.reply(result)

@Skoll.command()
async def multiply(ctx , arg1 : int  ,arg2 : int):
    product = arg1 * arg2
    await ctx.reply(product)


@Skoll.command()
async def divide(ctx , arg1 : int  ,arg2 : int):
    result = arg1 / arg2
    await ctx.reply(result)

@Skoll.command()
async def power(ctx , arg1 : int  ,arg2 : int):
    result = arg1 ** arg2
    await ctx.reply(result)




Skoll.run(TOKEN)