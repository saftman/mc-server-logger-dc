# mc-server-logger-dc

Welcome to mc-server-logger-dc! This is a Discord bot that allows you to log player join/leave events and display server information on Discord.

## Features

- Logs player join and leave events on your Minecraft server
- Displays server information such as description, player count, and version on Discord
- Provides player-specific information including last online time, playtime, and player head image

## Prerequisites

Before using the bot, make sure you have the following:

- Discord bot token: You need to create a Discord bot and obtain its token.
- Discord server and channel: Create a Discord server and channel where you want the bot to send the log messages.
- Minecraft server IP and port: Specify the IP address and port of your Minecraft server.

## Installation

1. Clone or download this repository.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Open the `bot.py` file and replace the following placeholders with your own values:
   - `TOKEN`: 'Your Discord bot token.'
   - `GUILD_ID`: 'Your Discord server ID.'
   - `CHANNEL_ID`: 'Your Discord channel ID.'
   - `SERVER_IP`: 'Your Minecraft server IP address.'
   - `SERVER_PORT`: 'Your Minecraft server port.'
4. Save the `bot.py` 'file after making the necessary changes.'
5. Run the bot using the command `python bot.py`.

## Usage

Once the bot is up and running, you can use the following commands on Discord:

- `!info`: Displays information about the Minecraft server, including the description, player count, and version.
- `!player [playername]`: Retrieves information about a specific player, including their last online time, playtime, and player head image.
- `!top`: Shows the top 10 players based on their playtime.

Feel free to customize the bot and its functionality according to your needs.

## Contributions

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the [MIT License](LICENSE).
