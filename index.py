#!/usr/bin/env python
#-*- coding: utf-8 -*-


import discord
import random
import datetime
import urllib
import re
import youtube_dl
import asyncio

from random import randint, choice
from discord.ext import commands, tasks
from urllib import parse, request

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)




bot = commands.Bot(command_prefix='¡', description="Hola zoy Franchesco, Fiauuuuu.")

@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(title="Franchesco BOT 1.0 by Ivan_44_up", description="Comandos disponibles:", timestamp=datetime.datetime.utcnow(), color=discord.Colour.from_rgb(255, 185, 0))
    embed.add_field(name="**¡adelantar**", value="``Muestra las posibilidades de que te adelante Franchesco``")
    embed.add_field(name="**¡azar**", value="``Minijuego en el que tienes que adivinar un número del 1 al 10``")
    embed.add_field(name="**¡stats**", value=f"``Estadisticas de {ctx.guild.name}``")
    embed.add_field(name="**¡yt**", value=f"``Busca videos en YouTube``")
    embed.add_field(name="**¡xxx**", value=f"``Busca videos en páginas +18``")
    embed.add_field(name="**¡ping**", value=f"``Te indica el ping actual del BOT``")
    embed.add_field(name="**¡p**", value=f"``Reproduce el video de YT que tu le indiques``")
    embed.add_field(name="**¡s**", value=f"``Para de reproducir el video de YT``")
    embed.add_field(name="**¡fiaun**", value=f"``Reproduce un sonido random``")
    embed.add_field(name="**Ping actual: **", value=f"{round(bot.latency * 1000)}ms")
    embed.add_field(name="**+ Info: **", value="https://www.zentergames.es/ o zenterstudios@gmail.com")
    embed.set_thumbnail(url="https://lh3.googleusercontent.com/NwhQS0-LoqBArZ6ePoiZ308NfK3F3FZpwfarQwsRTGb1icgsCFYlQVCJokssCqj56wA=w412-h732-rw")
    await ctx.send (embed=embed)

@bot.command()
async def adelantar(ctx):
    porcentaje = random.randint(100, 1000)
    
    await ctx.send ("Este es el % de que te adelante Franchesco:")
    await ctx.send (porcentaje)

@bot.command()
async def azar(ctx):
    await ctx.send ("Pon ¡num y un numero del 1 al 10 haber si aciertas cruck!!")

@bot.command()
async def stats(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Estadisticas del Server:", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    embed.add_field(name="Fecha de creación: ", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Dueño del server: ", value=f"{ctx.guild.owner}")
    embed.add_field(name="Región: ", value=f"{ctx.guild.region}")
    embed.add_field(name="ID del servidor: ", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url="https://i.ytimg.com/vi/n9k1_T9eq6g/maxresdefault.jpg")
    await ctx.send (embed=embed)

@bot.command()
async def yt(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

@bot.command()
async def xxx(ctx, *, search):
    query_string = parse.urlencode({'search': search})
    html_content = urllib.request.urlopen("https://es.pornhub.com/video/search?" + query_string)
    search_results = re.findall(r"view_video.php?(\S{24})", html_content.read().decode())
    await ctx.send('https://es.pornhub.com/view_video.php' + search_results[0])


@bot.command()
async def num(ctx, numero: int):
    numeroAlAzar = random.randint(1,10)

    if numero < 1:
        await ctx.send ("Eso es menor a 1, soy italiano pero no tonto.")
    else:
        if numero > 10:
            await ctx.send ("Eso es mayor a 10 ¿¿no crees??")
        else:
            if numero == numeroAlAzar:
                await ctx.send ("Acertaste el numero era:")
                await ctx.send (numeroAlAzar)
            else:
                await ctx.send ("Fallaste Paquete, el numero era:")
                await ctx.send (numeroAlAzar)

@bot.command()
async def ping(ctx):
    await ctx.send (f'**Pong!!!** Latencia: {round(bot.latency * 1000)}ms')

@bot.command()
async def p(ctx, *, url):
    if not ctx.message.author.voice:
        await ctx.send('**COMO QUIERES QUE TE PONGA MUSICA**,  **SI NO ESTAS** en ningun canal de **VOZ**')
        return

    else:
        channel = ctx.message.author.voice.channel
    
    
    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client
    await ctx.send("``Buscando en YouTube:`` **" + url + "**")

    
    
    async with ctx.typing():

        busqueda = parse.urlencode({'search_query': url})
        html = urllib.request.urlopen("https://www.youtube.com/results?" + busqueda)
        resultados = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url_final = ('https://www.youtube.com/watch?v=' + resultados[0])
        player = await YTDLSource.from_url(url_final, loop=bot.loop)
        voice_channel.play(player, after=lambda e: print('Error: %s' % e) if e else None)

    await ctx.send('**Estas Ezkuchando:** ' + url_final)

@bot.command()
async def fiaun(ctx):
    if not ctx.message.author.voice:
        await ctx.send('**COMO QUIERES QUE TE HAGA FIAUN**,  **SI NO ESTAS** en ningun canal de **VOZ**')
        return

    else:
        channel = ctx.message.author.voice.channel
    

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client
    

    
    
    async with ctx.typing():

        url_final = ["https://www.youtube.com/watch?v=iE3kD4X_Fwg&ab_channel=nwodyos%E3%83%80%E3%82%A6%E3%83%B3", "https://www.youtube.com/watch?v=bozUzubDPwM&ab_channel=CentralFbi"]
        player = await YTDLSource.from_url(choice(url_final), loop=bot.loop)
        voice_channel.play(player, after=lambda e: print('Error: %s' % e) if e else None)

    await ctx.send('**Fiauuuun, Franchesco  te ADELANTÓ PRRO** ')



@bot.command()
async def s(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    await ctx.send('**Me desconecte del canal de voz**')




           

                    





#events

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Adelantando a Makuin"))
    print('Franchesco Arranco los motores, Fiauuu.')


        
bot.run('remplace me')#Aqui pones el token de tu bot