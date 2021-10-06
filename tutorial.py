
from dotenv import load_dotenv
import discord
from discord.ext import commands,tasks

import json
import os

if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "!"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]

bot = commands.Bot(command_prefix=prefix)


load_dotenv()
# When new member is added to server
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has joined Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hello {member.name}!! Welcome to Our Discord Server!'
    )

client.run(TOKEN)


@bot.event
async def on_ready():
    print("Bot is ready.")


@bot.command()
# command for ping
async def ping(ctx):
    latent = round(bot.latency * 1000, 1)
    await ctx.send(f"Ping ! {latent}ms")


@bot.command()
# Say Hello to a particular member
async def hi(ctx, member):
    await ctx.send(f"Hello! {member}")


@bot.command()
# Ban a member
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):

    await member.ban(reason=reason)
    await ctx.send(f"{member} was banned!")

@bot.command()
@commands.has_permissions(kick_members=True)
# Kick a member
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} was kicked!")

@bot.command()
# Change activity of bot
@command.has_permissions(administrator=True)
async def activity(ctx,*,activity):
      await bot.change_presence(activity = discord.Game(name=activity))
      await ctx.send(f"Bot's activity changed to {activity}")

# Embed information about author

@bot.command()

async def embeduserinfo(ctx):
    user = ctx.author
    embed = discord.Embed(title="User Info",description = f"Here is the embedded info about {user}",colour= user.colour)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)


# Custom help command for discord bot

async def help(ctx,commandsent = None):
    if commandsent!=None:

         for command in bot.commands:
             if commandsent.lower()==command.name.lower():
                paramstr = ""
                for param in command.clean_params:
                    paramstr= paramstr + param + ", "

                paramstr = paramstr[:-2]


                if len(command.clean_params)==0:
                   paramstr = "None" 

                embed=discord.Embed(title=f"HELP - {command.name}", description=command.description)
                embed.add_field(name="parameters", value=paramstr)
                await ctx.message.delete()
                await ctx.author.send(embed=embed)
    else:

        embed=discord.Embed(title="HELP")
        embed.add_field(name="ping", value="Gets the bots latency", inline=False)
        embed.add_field(name="hi", value="Says hello to a specified user, Parameters: Member", inline=False)
        embed.add_field(name="embeduserinfo", value="Retreives info about the user", inline=False)
        await ctx.message.delete()
        await ctx.author.send(embed=embed)

        
@tasks.loop(seconds=10)
async def messageInterval(ctx, message):
    await ctx.send(message)


bot.run(token)
