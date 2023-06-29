import discord
import requests
import asyncio
from datetime import datetime

TOKEN = ''
GUILD_ID = ''
CHANNEL_ID = ''
SERVER_IP = ''
SERVER_PORT = ''

client = discord.Client()


def get_player_list():
    url = f"https://api.minetools.eu/query/{SERVER_IP}/{SERVER_PORT}"
    response = requests.get(url)
    data = response.json()
    players = data.get('Playerlist', [])
    return players


def get_server_info():
    url = f"https://api.minetools.eu/query/{SERVER_IP}/{SERVER_PORT}"
    response = requests.get(url)
    data = response.json()
    return data


async def send_embed_message(player, join_time):
    guild = client.get_guild(int(GUILD_ID))
    channel = guild.get_channel(int(CHANNEL_ID))

    # Get player skin image URL
    skin_url = f"https://mc-heads.net/avatar/{player}"

    embed = discord.Embed(title=f'{player} joined the Minecraft Server', color=discord.Color.green())
    embed.set_thumbnail(url=skin_url)
    embed.add_field(name='Player Name', value=player, inline=True)
    embed.add_field(name='Join Time', value=join_time, inline=True)

    await channel.send(embed=embed)


async def send_server_info():
    guild = client.get_guild(int(GUILD_ID))
    channel = guild.get_channel(int(CHANNEL_ID))

    server_info = get_server_info()

    embed = discord.Embed(title='Server Information', color=discord.Color.blue())
    embed.add_field(name='Description', value=server_info.get('Motd'), inline=False)
    embed.add_field(name='Players Online', value=server_info.get('Players'), inline=True)
    embed.add_field(name='Max Players', value=server_info.get('MaxPlayers'), inline=True)
    embed.add_field(name='Version', value=server_info.get('Version'), inline=False)

    player_list = server_info.get('Playerlist', [])
    if player_list:
        player_list_str = '\n'.join(player_list)
        embed.add_field(name='Players Online', value=player_list_str, inline=False)
    else:
        embed.add_field(name='Players Online', value='No players online', inline=False)

    await channel.send(embed=embed)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('------')


@client.event
async def on_message(message):
    if message.content == '!info':
        await send_server_info()


@client.event
async def check_player_list():
    await client.wait_until_ready()
    previous_player_list = []

    while not client.is_closed():
        current_player_list = get_player_list()

        if current_player_list != previous_player_list:
            for player in current_player_list:
                if player not in previous_player_list:
                    join_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    await send_embed_message(player, join_time)
            for player in previous_player_list:
                if player not in current_player_list:
                    leave_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    await send_embed_message(player, f'{leave_time} (left)')

        previous_player_list = current_player_list
        await asyncio.sleep(15)  # Check every 15 seconds


client.loop.create_task(check_player_list())
client.run(TOKEN)
