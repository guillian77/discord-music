#Import discord
import discord
from discord.ext import commands
 
# Import other modules
from asyncio import sleep
import youtube_dl
import os

path = '/home/gaspard/Projets/DiscordBot/'

# Create the bot prefix
bot = commands.Bot(command_prefix='!')

# Create playlist
playlist = []

TOKEN = os.getenv('DISCORD_TOKEN')

def ensure_dir(file_path):
    print(file_path)
    directory = path + "/" + file_path
    print(directory)
    if not os.path.exists(directory):
        os.mkdir(directory)

# Create a ping command
@bot.command()
async def ping(ctx):
    print('test')
    await ctx.send('pong')

# Setup the server
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    perms = discord.Permissions(send_messages=False, read_messages=True)
    await ctx.guild.create_role(name='Muted', permissions=perms)
    perms = discord.Permissions(administrator=True)
    await ctx.guild.create_role(name='Judge', permissions=perms) # <--- CHANGE THIS
    await ctx.send('The server is setted up!')
    print('A server is setted up!')

# Clear messages
@bot.command()
@commands.has_role('Judge')
async def clear(ctx, num):
    msg = []
    async for x in ctx.channel.history(limit=int(num)):
        msg.append(x)
    await ctx.channel.delete_messages(msg)
    print(num + ' messages removed from the channel')
    warning = await ctx.send(num + ' messages removed from the channel')

    # Wait to remove the warning message
    await sleep(3)
    await warning.delete()

# Ban users
@bot.command()
@commands.has_role('Judge')
async def ban(ctx, user: discord.Member):
    await user.ban()
    await ctx.send('The user has been banned')
    print('A user has been banned')

# Kick users
@bot.command()
@commands.has_role('Judge')
async def kick(ctx, user: discord.Member):
    await user.kick()
    await ctx.send('The user has been kicked out the server')
    print('A user has been kicked')

# Mute users
@bot.command()
@commands.has_role('Judge')
async def mute(ctx, user: discord.Member, time):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.add_roles(role)
    await ctx.send(str(user) + ' has been muted')
    print('A user has been muted')
    
    # Wait a certain time before unmuting
    await sleep(int(time))
    await user.remove_roles(role)
    await ctx.send(str(user) + ' is unmuted')
    print('A user has been unmuted')

@bot.command()
async def stop(ctx):
    channel = ctx.message.author.voice.channel
    await ctx.guild.voice_client.disconnect()
    await ctx.send('The song is stopped')

@bot.command()
async def play(ctx, chosenPlaylist):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    if voice.is_connected() and not voice.is_playing():
        ctx.guild.voice_client.play(discord.FFmpegPCMAudio("download.mp3"))
    await ctx.send("The song is playing")

@bot.command()
async def playUrl(ctx, url):
    await ctx.send("The song is downloading")
    # Join the channel
    # Join the channel
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()

    # Download as song.mp3
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    #Change to download.mp3
    for file in os.listdir("./"):
         if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "download.mp3")

    # Play the song
    ctx.guild.voice_client.play(discord.FFmpegPCMAudio("download.mp3"))
    await ctx.send("The song is playing")


@bot.command()
async def show(ctx, chosenPlaylist):
    print(playlist)
    print(playlist[chosenPlaylist])
    await ctx.send(playlist[chosenPlaylist])

@bot.command()
async def add(ctx, chosenPlaylist, url):
    await ctx.send("The song is downloading")

    # Download as song.mp3
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    #Change to download.mp3
    ensure_dir(chosenPlaylist)

    for file in os.listdir("./"):
         if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            filename = "./" + chosenPlaylist + "/" + name + ".mp3"
            os.rename(file, filename)


    playlist[chosenPlaylist][name] = name
#     ctx.guild.voice_client.play(discord.FFmpegPCMAudio(filename))

# Run the bot
if TOKEN:
    print('The bot is ready.')
    bot.run(TOKEN)
else:
    print('Token is missing.')
