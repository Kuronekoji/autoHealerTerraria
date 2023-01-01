# Terraria-AutoHealer
 This is a program written in Python using openCV, Tkinter and win32. This will display the health bar it is checking on the window after pressing start and will 
 check for your health to get below five hearts. Once it matches that your health is low, the H key will be pressed to drink a health potion (default keybinds)
 After H is pressed a timer will also start to countdown cooldown times.

 I was going to implement a way to check buffs / debuffs to account for cooldown, but got lazy as I had already cropped the healthbar out. Let me know if you 
 have any better ideas or implementations in this program.

######Notes 
-Your game resolution must be 1920x1080, otherwise the healthbar will not be found, this is to account for different monitors.
-If Terraria is not in focus when cooldown is being counted, this will throw the timers more offsync so try to only use this when you are actively fighting or AFK.
-Sometimes if the game is loading weird it may false trigger.

