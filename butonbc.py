import discord
import asyncio

async def execute_broadcast(interaction, guild):
    broadcast_message = "Visit our Website: **https://saxoleaks.com/**"

    # Sunucudaki tüm üyeleri almak için async for döngüsü kullanıyoruz
    members = []
    async for member in guild.fetch_members(limit=None):
        members.append(member)

    success_count = 0
    error_count = 0

    # Başlangıç embed mesajını gönder
    embed = discord.Embed(title="DM Broadcast Başlatıldı",
                          description="`⌛` DM Gönderim İlerlemesi",
                          color=0x00FF00)
    embed.add_field(name="`✅` Başarılı Gönderimler", value=f"```{success_count}```", inline=True)
    embed.add_field(name="`❌` Başarısız Gönderimler", value=f"```{error_count}```", inline=True)
    embed.timestamp = discord.utils.utcnow()
    
    report_message = await interaction.channel.send(embed=embed)

    async def update_report():
        updated_embed = discord.Embed(title="DM Gönderim İlerlemesi",
                                      description="`⌛` DM Gönderim İlerlemeye Devam Ediyor",
                                      color=0x00FF00)
        updated_embed.add_field(name="`✅` Başarılı Gönderimler", value=f"```{success_count}```", inline=True)
        updated_embed.add_field(name="`❌` Başarısız Gönderimler", value=f"```{error_count}```", inline=True)
        updated_embed.timestamp = discord.utils.utcnow()
        await report_message.edit(embed=updated_embed)

    # Her kullanıcıya DM gönderme (Yalnızca Administrator olmayanlar)
    for member in members:
        if not member.bot and not member.guild_permissions.administrator:
            try:
                await member.send(content=broadcast_message)
                success_count += 1
                print(f"Successfully sent DM to: {member}")
            except Exception as e:
                error_count += 1
                print(f"Couldn't send DM to: {member}")
                print(f"Error: {e}")

            # Embed'i her mesaj gönderiminden sonra güncelle
            await update_report()
            await asyncio.sleep(0.07)  # Her mesaj arasında 70 ms bekle

    # Son embed güncellemesi
    final_embed = discord.Embed(title="`✅` DM Gönderim Tamamlandı",
                                color=0x00FF00)
    final_embed.add_field(name="`✅` Başarılı Gönderimler", value=f"```{success_count}```", inline=True)
    final_embed.add_field(name="`❌` Başarısız Gönderimler", value=f"```{error_count}```", inline=True)
    final_embed.timestamp = discord.utils.utcnow()

    await report_message.edit(embed=final_embed)
