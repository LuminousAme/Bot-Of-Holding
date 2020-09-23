#import dotenv library
from dotenv import load_dotenv

#import os library
import os

#import SQLite3 library
import sqlite3

#import json library
import json

#import the discord library 
import discord

#import the commands extension 
from discord.ext import commands
#import the get extension
from discord.utils import get


#load bot secrets
loaddotenv()
TOKEN = os.getenv(BOT_TOKEN)

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

#generic function for accessing database
def open_database(**kwargs):
    conn = sqlite3.connect('boh.db')
    cursor = conn.cursor()

    #If inserting into inventory
    #If removing from inventory
    
    #Save changes then close the database    
    conn.commit()
    conn.close()

#******Bag of holding commands******
#give command
@client.command(aliases=['g', 'G', 'give'])
async def Give(ctx, user: str, item: str, amount: int):
    # Check if user exists
    # Check if author has item in the right amount
    # Transfer item from author record to user record

#list command
@client.command(aliases=['inventory', 'Inventory', 'list', 'l', 'L', 'i', 'I'])
async def List(ctx):
    # Find author
    # List items attached to author in inventory


#use command
@client.command(aliases=['u', 'U', 'use'])
async def Use(ctx, user: str, item: str):
    pass

#discard
@client.command(aliases=['d', 'D', 'discard'])
async def Discard(ctx, item: str, amount: int):
    # Find author
    # Find item in author inventory
    # Remove 'amount' of items from inventory

#empty
@client.command(aliases=['e', 'E', 'empty'])
async def Empty(ctx):
    # Find author
    # Revert inventory to {}

#allow the code to run on discord 
client.run(TOKEN)

