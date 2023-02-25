import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from threading import Thread
from asyncio import run

import datetime
import random
import json
import codecs
from ipwhois import IPWhois
from io import BytesIO

import config
from misc.misc import *
from misc.yt2mp3 import download

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', owner_ids = set(config.shell_users), description=config.bot_description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def subtract(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left - right)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def ipwhois(ctx, ip: str):
    obj = IPWhois(ip)
    results = json.dumps(obj.lookup_whois(), indent=4)
    await ctx.send(results)

@bot.command()
async def uptime(ctx):
    await ctx.send("System uptime: " + get_uptime())

@bot.command()
async def xmas(ctx):
    currentdate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    xmasmsg = "There are %s days until Christmas!" % (days_to_xmas(datetime.datetime.strptime(currentdate, '%Y-%m-%d')))
    await ctx.send(xmasmsg)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello %s!" % ctx.message.author.mention)

@bot.command()
async def mball(ctx):
    answers = ['It is certain', 'It is decidedly so', 'Without a doubt', \
        'Yes - definitely', 'You may rely on it', 'As I see it, yes',\
        'Most likely', 'Outlook good', 'Signs point to yes', 'Yes', \
        'Reply hazy, try again', 'Ask again later', 'Better not tell you now', \
        'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', \
        'My reply is no', 'My sources say no', 'Outlook not so good', \
        'Very doubtful'
    ]
    random.shuffle(answers)
    response = 'Magic Ball says: ' + random.choice(answers)
    await ctx.send(response)

@bot.command()
async def rot13decode(ctx, *, args):
    text = codecs.decode(args, 'rot_13')
    await ctx.send('Plaintext of rot13 "%s" is: %s' % (args, text))

@bot.command()
async def rot13encode(ctx, *, args):
    rot13 = codecs.encode(args, 'rot_13')
    await ctx.send('Rot13 of "%s" is: %s' % (args, rot13))

@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar.url
    await ctx.send(userAvatarUrl)

@bot.command()
async def url2img(ctx, *,  url : str):
    async with aiohttp.ClientSession() as session: # creates session
        async with session.get(url) as resp: # gets image from url
            img = await resp.read() # reads image from response
            with io.BytesIO(img) as file: # converts to file-like object
                await channel.send(file=discord.File(file, "testimage.png"))

def ytdl(ctx, url):
    ytdl = download(url)
    file = ytdl[0]
    title = ytdl[1]
    ytid = ytdl[2]
    with open(file, "rb") as fh:
        buf = BytesIO(fh.read())
        bot.loop.create_task(ctx.send("Filename is %s.mp3" %(ytid), file=discord.File(buf, title+'.mp3')))

@bot.command()
async def yt2mp3(ctx, *,  url : str):
    await ctx.send("Downloading video and converting to mp3...")
    background_thread = Thread(target=ytdl, args=(ctx,url,))
    background_thread.start()

@bot.command()
async def playmp3(ctx, *, file : str):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio('downloads/'+file)
    voice.stop()
    player = voice.play(source)  

@bot.command()
async def stopmp3(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await ctx.send("Stopped mp3 playback.")
        voice.stop()

@bot.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()

run(bot.load_extension('dshell'))
bot.dshell_config['shell_channels'] = config.shell_channels # put your own channel IDs here. all the channels that you've put will become shell channels
bot.dshell_config['give_clear_command_confirmation_warning'] = False

bot.run(config.bot_token)