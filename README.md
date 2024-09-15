This program is a discord bot RAT (Remote Access Trojan) that is slightly inspired off PySilon.   

I made this for fun bc im board.

Yes it's technicaly malware.

This program has the added bonus of not needing admin permisions(for windows, idk about mac and linux)

From what I researched this should only support 1 bot conection at a time but from testing i learned it can support 3 but maybe more
___
List of commands:

  Define target:
  
  When using this RAT you must use the id prefix after the command to direct the bot to activate when called, example: !test jimmy
  
  * "target id"(The name that shows when the bot is activated)= sends only to the target id and the prefix "dir" will be used when replying to the server
    
  * all = send to all active bots and no prefix will be used only sending the command output string
  
  * other/blank/mistype = print 0 / does nothing 
___
  Commands:
  
   The target must be called after the command or the command will be nullifyed. !example jimmy afterstring {file atachment}
    
   Certain commands suport and afterstring which changes the ouput this will be indecated below with (str)
    
   Certain commands require a file atachment (example: openimg) if not provided the desired output will not be achived, they will be indecated with (file)
   
   * !stop = turns of script/bot 
   
   * !test = test if online, the receive type and version
   
   * !screen = screenshot 
   
   * !write (str)= opens notepad and types on it, if afterstring isn't provided it will just print a predefined message 
   
   * !sendurl (str)= opens the directed url, if none idk what happens
   
   * !rick = opens youtube rick roll
   
   * !altrick = opens youtube animated rick roll
   
   * !openimg (file)= opens the image file atached with the command
   
   * !prompt (str)= sends a prompt where you have to click ok, clicking ok does nothing
   
   * !wallpaper (file)(str)= changes the wallpaper of the target to the image file, if the afterstring is "perm" the change persists after restarting else it doen't
   
   * !audio (file)= plays the attached audio file
   
   * !extra = helps with development same as !test but without version indecation
___
💀Slightly dangerous commands if the person using them has ill intent💀

These are indecated in the bot with skull emoji's after command is called (💀history💀:)

*!history = shows google chrome history

*!grabip = grabs users public ip
___
Older versionns will not suport newer commmands

To bundle to an exe use pyinstaller

On targets computer, to deactivate the RAT use task manager or simular tools

On targets computer, to remove the RAT just deactivate, and remove the exe or script as its only 1 file

If you need help discord handle or other comunication method will be attached later
