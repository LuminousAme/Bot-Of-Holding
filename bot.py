#import logging library
import logging

#import os library
import os

#import SQLite3 library
import sqlite3

#import json library
import json

#import the discord library 
import discord

#import dotenv library
from dotenv import load_dotenv
#import the commands extension 
from discord.ext import commands
#import the get extension
from discord.utils import get


#load bot secrets
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

#set up logging file
logging.basicConfig(filename='log.txt', filemode='a', 
                    format='%(asctime)s %(msecs)d- %(process)d-%(levelname)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S %p' ,
                    level=logging.DEBUG)

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

#generic functions for adding users
def add_user(user, *arg):
    connec = sqlite3.connect('boh.db')
    cursor = conn.cursor()
    if len(arg) > 0:
        inv = json.dump({arg})
    else:
        inv = json.dump({})
    to_insert = (user, inv,)
    cursor.execute('INSERT INTO boh VALUES (?,?)', to_insert)
    #Save changes then close the database    
    connec.commit()
    connec.close()
    print(user + " added to database.")
    logging.info(user + " added to database.")

#generic function for accessing & modifying inventories
def access_db(command,author,**kwargs):
    connec = sqlite3.connect('boh.db')
    cursor = conn.cursor()

    #find author in database
    if cursor.execute('SELECT Inventory FROM boh WHERE UserID=?', (author,)):
        if (command == 'give') or (command == 'discard'):
            inv = json.load(cursor.fetchone())
            #check if item in author inventory
            if kwargs['item'] in inv:
                #check if there is enough to remove
                if inv[kwargs['item']] >= kwargs['amount']:
                    #remove item from author inventory 
                    inv[kwargs['item']] = inv[kwargs['item']] - kwargs['amount']
                    #if amount of items is reduced to 0, remove it completely
                    if inv[kwargs['item']] == 0:
                        inv.pop(kwargs['item'])
                    # Update inventory
                    inv = json.dump(inv)
                    cursor.execute('UPDATE bot SET Inventory = ? WHERE UserID=?', (inv, author,))
                    #Save changes then close the database    
                    connec.commit()
                    connec.close()
                else:
                    return "wrong_amount"
            else:
                return "not_in"
            #insert item into to_give[user] inventory
            if command == 'give':
                #check if user in database
                if cursor.execute('SELECT Inventory FROM boh WHERE UserID=?',
                        (author,)):
                    inv = json.load(cursor.fetchone())
                     #check if item in user inventory
                    if kwargs['item'] in inv:
                        # Increase amount of items
                        inv[kwargs['item']] == inv[kwargs['item']] + kwargs['amount']
                    else:
                        # Add item to inventory
                        inv.update({kwargs['item']: kwargs['amount']})
                        inv = json.dump(inv)
                # If not in database, add the user
                else:
                    inv = json.dump({kwargs['item']: kwargs['amount']})
                    add_user(kwargs['user'], inv)
        elif command == 'inventory':
            #return inventory
            return cursor.fetchone()
        elif command == 'empty':
            cursor.execute('UPDATE boh SET Inventory = "{}" WHERE UserID=?',
                                (author,))
            #Save changes then close the database    
            connec.commit()
            connec.close()
            return 'success_empty'
    #if author doesn't exist make a new entry
    else:
        add_user(kwargs['user'])

#******Bag of holding commands******
#give command
@client.command(aliases=['g', 'G', 'give'])
async def Give(ctx, user: discord.User, item: str, amount: int):
    # Check if user exists
    ##NEED TO FIX HOW TO CHECK FOR DISCORD USER
    if guild.member(discord.User):
        print('hello')
        guild = ctx.guild
        author = ctx.author.id
        to_give = {'user': discord.Member.id, 
                        'item': item, 'amount': amount}
        # If user exists, transfer the item   
        access_db('give',author,to_give)
        ##NEED TO ADD WHAT TO DO WITH ERRORS
    else:
        await ctx.send(user + " is not in this server.")
        print(user + " is not in this server.")
        logging.info(user + " is not in this server.")

#list command
@client.command(aliases=['inventory', 'Inventory', 'list', 'l', 'L', 'i', 'I'])
async def List(ctx):
    # Find author
    author = ctx.author.id
    inv = access_db('inventory', author)
    # List items attached to author in inventory
    if (inv != 1) or (inv != []):
        for item in inventory:
            await ctx.send(item)
    else:
        await ctx.send("You don't anything in your inventory.")

#use command
@client.command(aliases=['u', 'U', 'use'])
async def Use(ctx, user: str, item: str):
    #discard only 1 of item
    to_discard = {'user': user.id, 'item': item, 'amount': 1}
    access_db('discard', to_discard)
    ##ADD WHAT DO DO WITH ERRORS

#discard
@client.command(aliases=['d', 'D', 'discard'])
async def Discard(ctx, item: str, amount: int):
    author = ctx.author.id
    print(author + "")
    # Discard amount of item from user inventory
    result = access_db('discard')
    ##ADD WHAT TO DO WITH ERRORS
        

#empty
@client.command(aliases=['e', 'E', 'empty'])
async def Empty(ctx):
    # Check they actually want to do this
    message = await ctx.send("Are you sure that you want to empty your inventory?")
    ##ADD REACTIONS
    ##ADD WHAT TO DO WITH ADDED REACTIONS
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji)
    ##ADD WHAT TO DO IF THEY SAY YES
    ##ADD WHAT TO DO WITH ERRORS

#allow the code to run on discord 
client.run(TOKEN)

