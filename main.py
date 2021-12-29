import asyncio
import discord
from discord.ext import commands
import keep_alive
from discord.ext.commands import Bot, has_permissions, CheckFailure

prefix = "+"
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name="+commands --> help"))
  print("Zockbot is ready!")

@bot.event
async def on_message (message):
  print("The message's content was", message.content)
  await bot.process_commands(message)


#+nuke
@bot.command()
@has_permissions(administrator=True)
async def nuke(ctx, amount=1):
  embed = discord.Embed(title="Zockerwolf76's NukeBot", color=0x800080)
  embed.add_field(name="How to setup and use:", value="1. Add the Bot by using this:  [link](https://discord.com/api/oauth2/authorize?client_id=863435929271271424&permissions=8&scope=bot)")
  embed.add_field(name=" ︎", value="2.Type !Nuke to start")
  await ctx.channel.purge(limit=amount)
  await ctx.send(embed=embed)


#+zockbot
@bot.command()
@has_permissions(administrator=True)
async def zockbot(ctx, amount=1):
  embed = discord.Embed(title="Zockerwolf76's Zockbot",description="This Bot isn't finished yet!", color=0x800080)
  embed.add_field(name="How to setup:", value="Add me by using this:  [link](https://discord.com/api/oauth2/authorize?client_id=890362274617917480&permissions=8&scope=bot)")
  await ctx.channel.purge(limit=amount)
  await ctx.send(embed=embed)


#+todo
@bot.command()
@has_permissions(administrator=True)
async def todo(ctx, amount=1):
  embed = discord.Embed(title="To Do List for Zockbot:", color=0x800080)
  embed.add_field(name=" ︎", value="1. Add more Commands")
  embed.add_field(name=" ︎", value="2. ...")
  await ctx.channel.purge(limit=amount)
  await ctx.send(embed=embed)


#+clear
@bot.command()
@has_permissions(administrator=True)
async def clear(ctx, amount=100):
  await ctx.channel.purge(limit=amount)


#+ban
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
  await user.ban(reason=reason)
  ban = discord.Embed(title=f":boom: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
  await ctx.message.delete()
  await ctx.channel.send(embed=ban)
  await user.send(embed=ban)

#+kick
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
  await user.kick(reason=reason)
  kick = discord.Embed(title=f":boom: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
  await ctx.message.delete()
  await ctx.channel.send(embed=kick)
  await user.send(embed=kick)

#+tempmute
@bot.command()
@commands.has_permissions(manage_messages=True)
async def tempmute(ctx, member: discord.Member,time):
 
  muted_role=discord.utils.get(ctx.guild.roles, name="Muted")
  time_convert = {"s":1, "m":60, "h":3600,"d":86400}
  tempmute= int(time[0]) * time_convert[time[-1]]
  await ctx.message.delete()
  await member.add_roles(muted_role)
  embed = discord.Embed(description= f"✅ **{member.display_name}#{member.discriminator} muted successfuly for {time}**", color=0x800080)
  await ctx.send(embed=embed, delete_after=5)
  await asyncio.sleep(tempmute)
  await member.remove_roles(muted_role)

#+unmute
@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
  mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
  await member.remove_roles(mutedRole)
  await member.send(f" you have unmutedd from: - {ctx.guild.name}")
  embed = discord.Embed(title="unmute", description=f" {member.mention} got unmuted",color=0x800080)
  await ctx.send(embed=embed)

#+mute
@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
  guild = ctx.guild
  mutedRole = discord.utils.get(guild.roles, name="Muted")
  embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", color=0x800080)
  embed.add_field(name="reason:", value=reason, inline=False)
  await ctx.send(embed=embed)
  await member.add_roles(mutedRole, reason=reason)
  await member.send(f" you have been muted from: {guild.name} reason: {reason}")


#+commands
@bot.command()
async def commands(ctx, amount=1):
  embed = discord.Embed(title="All Zockbot commands:", color=0x800080)
  embed.add_field(name=" ︎", value=" ︎")
  embed.add_field(name="Administrator commands:", value=" ︎")
  embed.add_field(name=" ︎", value="+nuke - get invite link for my Nuke Bot")
  embed.add_field(name=" ︎", value="+zockbot - get my invite link")
  embed.add_field(name=" ︎", value="+todo - to Do List for Zockbot")
  embed.add_field(name=" ︎", value="+clear - clear Last 100 messages")
  embed.add_field(name=" ︎", value="+kick @(user) (reason) - kick a user from the server")
  embed.add_field(name=" ︎", value="+ban @(user) (reason) - ban a user from the server")
  embed.add_field(name=" ︎", value="+tempmute @(user) (time s,m,h,d) - Mutes a user for a specific time")
  embed.add_field(name=" ︎", value="+mute @(user) (reason) - mutes a specific user")
  embed.add_field(name=" ︎", value="+unmute @(user) - unmutes a specific muted user")
  embed.add_field(name=" ︎", value="(more soon)")
  embed.add_field(name=" ︎", value=" ︎")
  embed.add_field(name="commands for everyone:", value=" ︎")
  embed.add_field(name=" ︎", value="+commands - list of all commands")
  embed.add_field(name=" ︎", value="(more soon)")
  await ctx.channel.purge(limit=amount)
  await ctx.send(embed=embed)

  
  
keep_alive.keep_alive()
bot.run('ODkwMzYyMjc0NjE3OTE3NDgw.YUusfA.JfEgurc7LMZ2rgTQjqpZqlOslLg')