This program is a discord bot **RAT (Remote Access Trojan)** that is slightly inspired off PySilon.   

I made this for fun bc im board.

Yes it's technicaly malware.

This program has the added bonus of **not needing** admin permisions but running with admin will change the effects(for windows, idk about mac and linux)

This bot can **apparently* host up to 1000 users but I wasn't able to text it out
___
*****Warning:***** 
⚠️This bot is for Educational perposes only, i'm not liable for any damages caused by the person controling and/or modification to my code (you shouldn't be running suspicious files anyway)⚠️

**Changes admin permisions cause**

*Slighty dangerous commands no longer notify the user opon use (but more dangerous commnands added later still will)(But also why would you run suspicious exe's as admin)

*Changes the effects for certain commands (!wallpaper, ect)

**Info the RAT collects by default:**

*Users/Account username (This is so the you can direct commands to ceratin users & indirectly prevents your bot from getting rate limited(kinda))

*Slight changes if used in admin(nothing terrible)(no info collected by running in admin)

**Info the RAT can collect:**

*Public ip address

*Google chrome default search history

*sends screenshots

**More WILL be added**
___
List of commands info:

  Define target:
  
  When using this RAT you must use the id prefix after the command to direct the bot to activate when called, example: !test jimmy
  
  * "target id"(The name that shows when the bot is activated)= sends only to the target id and the prefix "dir" will be used when replying to the server
    
  * all = send to all active bots and no prefix will be used only sending the command output string

  * "group name" = the !group command allows you to put people in groups so can send actions to 2+ people without sending to all
  
  * other/blank/mistype = print 0 / does nothing 
___
Events

* On startup = sends a message to the hosts server and notifies the user so they know its on and don't spam opening the file and know its running
___
  Commands:
  
   The target must be called after the command or the command will be nullifyed or crash. Example: !test jimmy afterstring {file atachment}
    
   Certain commands suport an afterstring which changes the ouput this will be indecated below with (str)
    
   Certain commands require a file atachment (example: openimg) if not provided the desired output will not be achived, they will be indecated with (file)
   
   * !stop = turns of script/bot 
   
   * !test = test if online, the receive type and version

   * !debug (str)= toggles sending messages back to the user for commands that don't need to send somthing back (dissabled by default)

   * !group (str)= adds the selected user to a group making it easier to send commands to 2+ people but not all(also can prevent ratelimiting)

   * !listgroup = lists all the groups the user is assigned to
   
   * !screen = screenshot 
   
   * !write (str)= opens notepad and types on it, if afterstring isn't provided it will just print a predefined message (only windows)
   
   * !sendurl (str)= opens the directed url, if none idk what happens
   
   * !rick = opens youtube rick roll
   
   * !altrick = opens youtube animated rick roll clip
   
   * !openimg (file)= opens the atached image file as a window
   
   * !prompt (str)= sends a prompt where you have to click ok or close, clicking ok does nothing (for now)
   
   * !wallpaper (file)(str)= changes the wallpaper of the target to the image file but is only temporary (doesn't persist after restart)
     /w Admin = sets the images as the permanent wallpaper until changed by user (persists after restart)
   
   * !audio (file)= plays the attached audio file (only .mp3 and supposedly .wav)

   * !popimg (file)= overlays all the attached images on the users screen and they can click them to make them disapear
   
   * !extra = helps with development does nothing
___
💀 **Slightly dangerous commands (if the person using them has ill intent)** 💀

These are indecated in the bot with skull emoji's after opon the receving message command (💀history💀:)

These will also notify the user in a prompt, **Unless** the user enabled with admin perms (again why)

*!history = shows google chrome defaut history

*!grabip = grabs users public ip

*!autoswap = swaps the autotroll variable (autovar) to true or false (dissabled by default)

*!autotroll = if autovar is true then it will automaticaly cycle through commands (including slightly dangerous commands)
___
Note:

This RAT mainly works on windows as i can't test mac or linux

Older versionns will not suport newer commmands

To bundle to an exe use pyinstaller(will add a guide to how to do so later)

To deactivate the RAT use task manager or simular tools

To remove the RAT just deactivate, and remove the exe or script as its only 1 file + other files that have been sent

If you need help discord handle or other comunication method will be attached later
