import discord
import sys
import time
from discord.ext import commands
from discord.ext.commands import Bot

TOKEN = open("token.txt", "r").read()
client = Bot(command_prefix="$", intents=discord.Intents.default())

client.modules = ['bsctools', 'jishaku']

    
@client.event
async def on_ready():
    for module in client.modules:
        try:
            client.load_extension(module)
            print(f"Module {module} loaded")
        except Exception as e:
            print(f"Module {module} failed to load: {e}")
    print("Bot started")


@client.command(name='ping')
async def ping(context):
    beforeping = time.monotonic()
    messageping = await context.send("Pong!")
    pingtime = (time.monotonic() - beforeping) * 1000
    await messageping.edit(content=f"Pong! `{int(pingtime)}ms`")


@client.command(name='shutdown', hidden=True)
@commands.is_owner()
async def shutdown(context):
    # Remove nickname and presence when shutting down
    price_guild = client.get_guild(696082479752413274)
    await price_guild.me.edit(nick=None)
    await client.change_presence(activity=discord.Game(""))
    await context.message.add_reaction(u"\U00002705")  # Green checkmark
    sys.exit()


@client.command(name='load')
@commands.is_owner()
async def load(context, extension):
    try:
        client.load_extension(extension)
        await context.message.add_reaction(client.check)
    except Exception as e:
        try:
            await context.send(e)
        except discord.errors.HTTPException as e:
            print(e)
            await context.send("Error exceeds Discord character limit. See console for details.")


@client.command(name='unload')
@commands.is_owner()
async def unload(context, extension):
    client.unload_extension(extension)
    await context.message.add_reaction(u"\U00002705")


@client.command(name='reload')
@commands.is_owner()
async def reload(context, extension):
    try:
        client.unload_extension(extension)
        client.load_extension(extension)
        await context.message.add_reaction(u"\U00002705")
    except Exception as e:
        try:
            await context.send(e)
        except discord.errors.HTTPException as e:
            print(e)
            await context.send("Error exceeds Discord character limit. See console for details.")


@client.command(name='purge')
async def purge(context, amount):
    await context.message.add_reaction('\U0001F504')
    messages = []
    async for message in context.channel.history(limit=int(amount) + 1):
        messages.append(message)
    await context.channel.delete_messages(messages)

client.run(TOKEN)
