import os
import discord
import datetime
import requests
import logging


from random import randrange

from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure

from dotenv import load_dotenv
logging.basicConfig(level=logging.INFO)


load_dotenv()
config = {
    'token': os.environ['TOKEN'],
    'server_id': os.environ['SERVER_ID'],
    'channel_id': os.environ['CHANNEL_ID']
}

#GUILD_ID = ''

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    #data = requests.get(SERVER_METRICS).json()
    date = datetime.datetime.now()
    if config['channel_id']:
        get_data.start()
    print(f'[{date}] Bot aktywowany pomyślnie.')
    

@bot.event
async def on_disconnect():
    date = datetime.datetime.now()
    print(f'[{date}] Odebrano sygnał rozłączenia. Rozłączam...')

@bot.event
async def on_resumed():
    date = datetime.datetime.now()
    print(f'[{date}] Laczenie ponowne')

@bot.event
async def on_command_error(ctx, error):
    pass

    
# CONFIG COMMANDS
@bot.command(name='start', pass_context=True)
@has_permissions(administrator=True)
async def start_bot(ctx):
    guild_id = ctx.message.guild.id
    try:
      if not get_data.is_running():
        get_data.start()        
        await ctx.send('Zainicjowano pomyślnie. Użyj polecenia !setchannel \
<ID_kanału>, aby zmienić kanał głosowy, na którym będą wyświetlane dane serwera.')
    except Exception as ex:
        print(f'Wystąpił błąd podczas uruchamiania bota! {ex}')
        await ctx.send('Wystąpił błąd. Sprawdź dzienniki serwera pod kątem \
więcej informacji.')

@tasks.loop(minutes=10.0)
async def get_data():
    try:
        channel_players = bot.get_channel(int(config['channel_id']))
        server_id = config['server_id']
        data = requests.get(f'https://api.battlemetrics.com/servers/{server_id}').json()
        current_map = data['data']['attributes']['details']['map']
        players = data['data']['attributes']['players']
        status = data['data']['attributes']['status']
        await channel_players.edit(name=f'📱 {players}/100 - {current_map}')
        date = datetime.datetime.now()
        bm_data = data['data']['attributes']['updatedAt']
        print(f'Aktualizacja: [{date}] {current_map} {players}/100')
        print(f'BattleMetrics: {bm_data}')
        if status == "online":
          statuspic = "🟢"
        else:
          statuspic = "🔴"


      
        embed=discord.Embed(
    title="Serwer Old Stagers",
        url="https://www.battlemetrics.com/servers/hll/13496167",
        description="Zapraszamy do rozgrywki",
        color=discord.Color.blue())
        embed.set_author(name="ServerStatusBot", url="",       icon_url="https://i.ibb.co/QQHjdSW/950-E8-DF2-EBE2-478-E-B1-E2-E9118-B132-A7-E.png")
    #embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://i.ibb.co/QQHjdSW/950-E8-DF2-EBE2-478-E-B1-E2-E9118-B132-A7-E.png")
        embed.add_field(name="**[PL/ENG] Polish CREW - Polska SSO & WaTaHa**", value=f"Aktualni gracze: {players} /100", inline=False)
        embed.add_field(name="Status serwera:", value=f"{statuspic}", inline=False)
        embed.add_field(name="Aktualna Mapa: ", value=f"{current_map}", inline=False)
        embed.add_field(name="Ostatnie Odswiezenie: ", value=f"{bm_data}", inline=False)
        embed.add_field(name="Secrets", value="||Amper to koks||", inline=False)
        embed.set_footer(text="created by Krzysieg")
        message = await channel_players.send(embed=embed)
        message_ID = message.id
        

    except Exception as ex:
      print(f'Blad przy tworzeniu wiadomosci {ex}')

try:
    bot.run(config['token'], reconnect=True)
    
except Exception as ex:
    req = requests.get('https://discord.com/api/path/to/the/endpoint')
    req.headers["X-RateLimit-Remaining"]
    print(f'Blad przy inicjalizacji {ex}')
