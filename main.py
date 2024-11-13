import discord
from discord.ext import commands
import asyncio
from butonbc import execute_broadcast
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True  # guild_members yerine members kullanıldı

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} olarak giriş yaptı!")

@bot.event
async def on_guild_join(guild):
    guild_info = {
        "name": guild.name,
        "members": guild.member_count,
        "owner": guild.owner
    }

    embed = discord.Embed(title="Yeni bir sunucuya katıldım!",
                          description="Sunucu bilgileri aşağıda verilmiştir:",
                          color=0x00FF00)
    embed.add_field(name="Guild Name", value=guild_info["name"], inline=False)
    embed.add_field(name="Guild Members", value=guild_info["members"], inline=False)
    embed.add_field(name="Guild Owner", value=guild_info["owner"], inline=True)
    embed.timestamp = discord.utils.utcnow()

    row = discord.ui.View()
    row.add_item(discord.ui.Button(label="Broadcast", style=discord.ButtonStyle.primary, custom_id=f"broadcast_button_{guild.id}"))

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=embed, view=row)
        print(f"Mesaj başarılı bir şekilde config kanalına gönderildi: {guild.name}")
    else:
        print(f"Belirtilen kanal metin tabanlı değil veya erişilemez: {CHANNEL_ID}")

@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component and interaction.data["custom_id"].startswith("broadcast_button"):
        await interaction.response.defer(ephemeral=True)  # Zaman aşımını önlemek için işlem bekletiliyor
        guild_id = int(interaction.data["custom_id"].split("_")[2])
        guild = bot.get_guild(guild_id)
        
        if guild:
            await execute_broadcast(interaction, guild)
            await interaction.followup.send("Broadcast başarılı!", ephemeral=True)
        else:
            await interaction.followup.send("Sunucu bulunamadı.", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if not message.content.startswith(PREFIX):
        return

    args = message.content[len(PREFIX):].strip().split()
    command_name = args.pop(0).lower()

    if command_name in bot.commands:
        command = bot.get_command(command_name)
        if command:
            await bot.invoke(message)

bot.run(TOKEN)
