import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté comme {bot.user}")

bot.run(MTUxOTI3NzAxNzk0MDQ5NjQzNA.GRtjTr.TcZn_u6OOpgnx2djVzbcJZJyy8ZK93Hhn5WM1A)
