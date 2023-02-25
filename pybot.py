import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get


from asyncio import run

import config
import random
from ipwhois import IPWhois
import json
import datetime
import codecs
from yt2mp3 import download
from io import BytesIO


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime = secondsToText(uptime_seconds)

    return uptime

def secondsToText(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60
    result = ("{} days, ".format(int(days)) if days else "") + \
    ("{} hours, ".format(int(hours)) if hours else "") + \
    ("{} minutes, ".format(int(minutes)) if minutes else "") + \
    ("{} seconds, ".format(int(seconds)) if seconds else "")
    return result

def get_christmas(date):
    """Returns the date of the Christmas of the year of the date"""
    next_xmas = datetime.datetime(date.year, 12, 25)
    if next_xmas < date:
        next_xmas = datetime.datetime(date.year+1, 12, 25)
    return next_xmas

def days_to_xmas(input_date):
    ans = (get_christmas(input_date) - input_date).days
    return ans

description = 'pybot'
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
owners = [1076273465906167878, 591770524380692511, 1076273476979150998]
bot = commands.Bot(command_prefix='?', owner_ids = set(owners), description=description, intents=intents)

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

@bot.command()
async def yt2mp3(ctx, *,  url : str):
    await ctx.send("Downloading video and converting to mp3...")
    ytdl = download(url)
    file = ytdl[0]
    title = ytdl[1]
    ytid = ytdl[2]
    with open(file, "rb") as fh:
        buf = BytesIO(fh.read())
        await ctx.send("Filename is %s.mp3" %(ytid), file=discord.File(buf, title+'.mp3'))

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
    



#run(bot.load_extension('dshell'))
#bot.dshell_config['shell_channels'] = [1077653766821662740] # put your own channel IDs here. all the channels that you've put will become shell channels
#bot.dshell_config['give_clear_command_confirmation_warning'] = False

bot.run(config.token)