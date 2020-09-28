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
#logging.basicConfig(filename='log.txt', filemode='a', 
                    #format='%(asctime)s %(msecs)d- %(process)d-%(levelname)s - %(message)s', 
                    #datefmt='%d-%b-%y %H:%M:%S %p' ,
                    #level=logging.DEBUG)

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
async def Give(ctx, user: str, amount: int, item: str):
    user_id = user[3:-1]
    item = item.capitalize()
    author = str(ctx.author.id)
    print(author + ' requested to transfer ' + str(amount) + ' ' + item + ' to ' + str(user_id) + '.')
    # Open database
    connec = sqlite3.connect('boh.db')
    cursor = connec.cursor()
    # Find author in database
    cursor.execute('SELECT Inventory FROM boh WHERE UserID=?', (author,))
    inv_json = cursor.fetchone()
    if inv_json:
        #Load inventory
        inv = json.loads(inv_json[0])
        #check if item is in author inventory
        if item in inv:
            print(item + ' is in inventory')
            #check if there is enough to remove
            if inv[item] >= amount:
                print('There is enough to remove')
                #remove item from author inventory 
                inv[item] = inv[item] - amount
                #if amount of items is reduced to 0, remove it completely
                if inv[item] == 0:
                    inv.pop(item)
                # Update inventory
                inv_json = json.dumps(inv)
                cursor.execute('''UPDATE boh 
                        SET Inventory=? 
                        WHERE UserID=?''', (inv_json, author,))
                print('inventory updated')
                #check if user in database
                cursor.execute('SELECT Inventory FROM boh WHERE UserID=?', (user_id,))
                user_inv_json = cursor.fetchone()
                if user_inv_json:
                    user_inv = json.loads(user_inv_json[0])
                    #check if item in user inventory
                    if item in user_inv:
                        print('item in their inventory')
                        # Increase amount of items in inventory
                        user_inv[item] == user_inv[item] + amount
                        user_inv_json = json.dumps(inv)
                        cursor.execute('UPDATE boh SET Inventory = ? WHERE UserID=?', (user_inv_json,user_id,))
                        #Save changes then close the database    
                        connec.commit()
                        connec.close()
                        print('give successful')
                        await ctx.send("You sent " + user + " " + str(amount) + " " + item + "!")
                    else:
                        # Add item to inventory
                        print('item not in inventory')
                        user_inv.update({item: amount})
                        user_inv_json = json.dumps(user_inv)
                        cursor.execute('UPDATE boh SET Inventory = ? WHERE UserID=?', (inv,user_id,))
                        #Save changes then close the database    
                        connec.commit()
                        connec.close()
                        await ctx.send(str(amount) + ' ' + item + ' transferred successfully.')
                        print(str(amount) + ' ' + item + 'transferred from ' + author + ' to ' + str(user_id) + '.')
                # If not in database, add the user
                else:
                    print('user doesn\'t exist')
                    print(type(user_id)])
                    user_inv = {item: amount}
                    user_inv_json = json.dumps(user_inv)
                    # Add user to database
                    cursor.execute('INSERT INTO boh VALUES (?,?)', (user_id, user_inv_json,))
                    #Save changes and close the database
                    connec.commit()  
                    connec.close()
                    await ctx.send(user + ' added to database with ' + str(amount) + ' ' + item + '.')
                    print(user + ' added to database with ' + str(amount) + ' ' + item + '.')
            else:
                #Close database
                connec.close()
                await ctx.send('You do not have enough ' + item + ' to give ' + str(amount) + '.')
                print(author + ' doesn\'t have enough ' + item + ' to give.')
        else:
            #Close database
            connec.close()
            await ctx.send('You do not have ' + item + '.')
            print(author + ' doesn\'t have ' + item + '.')
    else:
        print('user does not exist')
        user_inv_json = json.dumps({})
        cursor.execute('UPDATE boh SET Inventory = ? WHERE UserID = ?', (user_inv_json,user_id,))
        #Save changes then close the database    
        connec.commit()
        connec.close()
        print('successful new user')
        await ctx.send("You don't have an inventory, created one for you.")

#list command
@client.command(aliases=['inventory', 'Inventory', 'list', 'l', 'L', 'i', 'I'])
async def List(ctx):
    author = str(ctx.author.id)
    print(author + ' requested to view their inventory.')
    # Open database
    connec = sqlite3.connect('boh.db')
    cursor = connec.cursor()
    # Find author in database
    cursor.execute('SELECT Inventory FROM boh WHERE UserID=?', (author,))
    inv_json = cursor.fetchone()
    if inv_json:
        inv = json.loads(inv_json[0])
        print(author + " inventory fetched.")
        # List items attached to author in inventory
        for item in inv:
            name = inv[item]
            await ctx.send(str(name) + ' ' + item)
        #Close database
        connec.close()
    else:
        print('nothing in inventory')
        #Close database
        connec.close()
        await ctx.send("You don't have anything in your inventory.")

#use command
@client.command(aliases=['u', 'U', 'use'])
async def Use(ctx, item: str):
    author = str(ctx.author.id)
    item = item.capitalize()
    print(author + ' requested to use ' + item + '.')
    # Open database
    connec = sqlite3.connect('boh.db')
    cursor = connec.cursor()
    # Find author in database
    cursor.execute('SELECT Inventory FROM boh WHERE UserID=?', (author,))
    inv_json = cursor.fetchone()
    if inv_json:
        #Load inventory
        inv = json.loads(inv_json[0])
        #check if item is in author inventory
        if item in inv:
            print(item + ' is in inventory')
            #check if there is enough to remove
            if inv[item] >= 1:
                print('There is enough to remove')
                #remove item from author inventory 
                inv[item] = inv[item] - amount
                #if amount of items is reduced to 0, remove it completely
                if inv[item] == 0:
                    inv.pop(item)
                # Update inventory
                inv_json = json.dumps(inv)
                cursor.execute('''UPDATE boh 
                        SET Inventory=? 
                        WHERE UserID=?''', (inv_json, author,))
                print('inventory updated')
                #Save changes then close the database    
                connec.commit()
                connec.close()
                print(item + ' used successfully.')
                await ctx.send(item + ' used successfully!')
            else:
                #Close database
                connec.close()
                print(author + ' doesn\'t have enough ' + item + ' in their inventory')
                await ctx.send("You don\'t have enough " + item + " in your  inventory")
        else:
            #Close database
            connec.close()
            print(author + ' doesn\'t have ' + item + ' in their inventory')
            await ctx.send("You don't have " + item + " in your inventory")

#discard command
@client.command(aliases=['d', 'D', 'discard'])
async def Discard(ctx, amount: int, item: str):
    author = str(ctx.author.id)
    item = item.capitalize()
    print(author + ' requested to discard ' + str(amount) + ' ' + item + '.')
    # Open database
    connec = sqlite3.connect('boh.db')
    cursor = connec.cursor()
    # Find author in database
    cursor.execute('SELECT Inventory FROM boh WHERE UserID=?', (author,))
    inv_json = cursor.fetchone()
    if inv_json:
        #Load inventory
        inv = json.loads(inv_json[0])
        #check if item is in author inventory
        if item in inv:
            print(item + ' is in inventory')
            #check if there is enough to remove
            if inv[item] >= amount:
                print('There is enough to remove')
                #remove item from author inventory 
                inv[item] = inv[item] - amount
                #if amount of items is reduced to 0, remove it completely
                if inv[item] == 0:
                    inv.pop(item)
                # Update inventory
                inv_json = json.dumps(inv)
                cursor.execute('''UPDATE boh 
                        SET Inventory=? 
                        WHERE UserID=?''', (inv_json, author,))
                print('inventory updated')
                #Save changes then close the database    
                connec.commit()
                connec.close()
                print(str(amount) + ' ' + item + ' discarded successfully.')
                await ctx.send(str(amount) + ' ' + item + ' discarded successfully!')
            else:
                #Close database
                connec.close()
                print(author + ' doesn\'t have enough ' + item + ' in their inventory')
                await ctx.send("You don\'t have enough " + item + " in your  inventory")
        else:
            #Close database
            connec.close()
            print(author + ' doesn\'t have ' + item + ' in their inventory')
            await ctx.send("You don't have " + item + " in your inventory")
                

#empty
@client.command(aliases=['e', 'E', 'empty'])
async def Empty(ctx):
    # Check they actually want to do this
    message = await ctx.send("Are you sure that you want to empty your inventory?")
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    def check(reaction, user):
        return user == ctx.author
    try:
        reaction, user = await client.wait_for("reaction_add", timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Timed out")
    else:
        print(reaction)
        if reaction == '✅':
            print("success??")
            print(type(reaction))
            author = str(ctx.author.id)
            # Open database
            connec = sqlite3.connect('boh.db')
            cursor = connec.cursor()
            # Find author
            cursor.execute('SELECT Inventory FROM boh WHERE UserID=?', (author,))
            inv_json = cursor.fetchone()
            if inv_json:
                # Empty inventory
                cursor.execute('UPDATE boh SET Inventory = "{}" WHERE UserID=?', (author,))
                #Save changes then close the database    
                connec.commit()
                connec.close()
                print('emptied successful')
            else:
                print('author doesn\'t exist')
                inv_json = json.dumps({})
                cursor.execute('UPDATE boh SET Inventory = ? WHERE UserID = ?', (user_inv_json,user_id,))
                #Save changes then close the database    
                connec.commit()
                connec.close()
                print('successful new user')
                await ctx.send("You don't have an inventory, created one for you.")
        elif reaction == '❌':
            await ctx.send("Inventory not emptied.")
        else:
            await ctx.send("Reaction not recognised.")

#allow the code to run on discord 
client.run(TOKEN)

