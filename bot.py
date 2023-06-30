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


async def send_player_info(player):
    guild = client.get_guild(int(GUILD_ID))
    channel = guild.get_channel(int(CHANNEL_ID))

    player_info = get_player_info(player)

    embed = discord.Embed(title='Player Information', color=discord.Color.green())
    embed.set_thumbnail(url=player_info['skin_url'])
    embed.add_field(name='Player Name', value=player, inline=True)
    embed.add_field(name='Last Online', value=player_info['last_online'], inline=True)
    embed.add_field(name='Playtime', value=f"{player_info['playtime']} minutes", inline=True)
    if player_info['online_status']:
        embed.add_field(name='Status', value='Online', inline=True)
    else:
        embed.add_field(name='Status', value='Offline', inline=True)

    await channel.send(embed=embed)


async def send_top_playtime():
    guild = client.get_guild(int(GUILD_ID))
    channel = guild.get_channel(int(CHANNEL_ID))

    filename = 'playertime.txt'

    try:
        with open(filename, 'r') as file:
            data = file.readlines()
            data = [line.strip().split(':') for line in data]
            data = sorted(data, key=lambda x: int(x[1]), reverse=True)
            top_players = data[:10]

            embed = discord.Embed(title='Top 10 Players by Playtime', color=discord.Color.gold())
            for i, player in enumerate(top_players):
                player_name, playtime = player
                embed.add_field(name=f'#{i + 1} {player_name}', value=f'Playtime: {playtime} minutes', inline=False)

            await channel.send(embed=embed)
    except FileNotFoundError:
        await channel.send('No playtime data available.')


def get_player_info(player):
    filename = 'playertime.txt'

    try:
        with open(filename, 'r') as file:
            data = file.readlines()
            for line in data:
                line = line.strip().split(':')
                if line[0] == player:
                    playtime = int(line[1])
                    return {
                        'playtime': playtime,
                        'last_online': line[2],
                        'online_status': line[3] == 'online',
                        'skin_url': f"https://mc-heads.net/avatar/{player}"
                    }
    except FileNotFoundError:
        pass

    return {
        'playtime': 0,
        'last_online': 'N/A',
        'online_status': False,
        'skin_url': f"https://mc-heads.net/avatar/{player}"
    }


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('------')


@client.event
async def on_message(message):
    if message.content == '!info':
        await send_server_info()
    elif message.content.startswith('!player'):
        player = message.content.split(' ')[-1]
        if player:
            await send_player_info(player)
        else:
            await message.channel.send('Please provide a player name.')
    elif message.content == '!top':
        await send_top_playtime()


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
