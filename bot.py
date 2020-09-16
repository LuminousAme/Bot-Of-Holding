#import the discord library 
import discord

#import the commands extension 
from discord.ext import commands
#import the get extension
from discord.utils import get


#set the command prefix for the bot 
client = commands.Bot(command_prefix = 'boh;')

#function for when the bot has all the info it needs and is ready to do stuff
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Fulfilling all your item holding needs'))
    print('Bot is ready.')

#generic function to catch errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That command does not exist.')


#******Bag of holding commands******
#give command
@client.command(aliases=['g', 'G', 'give'])
async def Give(ctx, user: str, item: str, amount: int):


#list command
@client.command(aliases=['inventory', 'Inventory', 'list', 'l', 'L', 'i', 'I'])
async def List(ctx):


#use command
@client.command(aliases=['u', 'U', 'use'])
async def Use(ctx, user: str, item: str):

#discard
@client.command(aliases=['d', 'D', 'discard'])
async def Discard(ctx, item: str, amount: int):
    

#empty
@client.command(aliases=['e', 'E', 'empty'])
async def Empty(ctx):
    

#allow the code to run on discord 
client.run('')

