import discord
from discord.ext import tasks, commands
import asyncio
import os
from flask import Flask

app = Flask(__name__)

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    auto_bump.start()

@tasks.loop(hours=2)
async def auto_bump():
    channel_id = int(os.getenv('BUMP_CHANNEL_ID'))  # Channel where !d bump works
    channel = bot.get_channel(channel_id)
    
    if channel:
        try:
            await channel.send('!d bump')
            print(f"Bump command sent at {discord.utils.utcnow()}")
        except Exception as e:
            print(f"Failed to send bump command: {e}")
    else:
        print("Channel not found")

@auto_bump.before_loop
async def before_auto_bump():
    print("Waiting for bot to be ready...")
    await bot.wait_until_ready()

# Health check endpoint for Render/UptimeRobot
@app.route('/')
def home():
    return "Bot is running!"

def run():
    from waitress import serve
    serve(app, host="0.0.0.0", port=10000)

if __name__ == '__main__':
    # Start Flask app in a separate thread
    import threading
    threading.Thread(target=run).start()
    
    # Start the bot
    bot.run(os.getenv('DISCORD_TOKEN'))
