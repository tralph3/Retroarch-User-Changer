# DO NOT USE THIS PROGRAM
This program is no more than an abandoned experiment that is most likely prone to failure. I would not recommend anyone to use it. Backing up folders manually is probably better than using this. I have no intentions of fixing this software. The proper solution would be a user system integrated in RetroArch itself, and I don't know if that's in their sights (probably not at the moment).

With that said, if you still want to use this, do so at your own risk. I recommend reading the code beforehand. No further development will take place. You have been warned.

# Retroarch User Changer
RetroArch, now for the whole family.

# What?
RetroArch User Changer is a simple program that lets you have multiple users in RetroArch. With its easy to use interface, you will be able to add users and swap their saves or configurations automatically in miliseconds. You will be able to have multiple separate menu configurations, RetroAchievements accounts, saves and savestates, screenshots and whatever else, each user with its own.

# How?
So, how does this work? Really simple. When you create an user, the configuration on the RetroArch folder will be copied over to that new user. You can create as many as you want. At this point, you should choose an user to set as active. When a user is set as active, the configuration on RetroArch gets copied over to the previously active user (unless there's no previous active user). Then, the configuration on RetroArch gets deleted and replaced with the one found on the new active user. So now, the next time you open RetroArch, you will find the configuration of the user you've set as active. Deleting a user will delete all of its configuration and save files. You have been warned.

# Could I risk losing save files?
Only if improperly used. It's important to understand what it's doing in the background to not lose data. The program will very often copy and delete files from the user's and RetroArch directories, but it won't do anything you don't tell it to do. For example, you can choose to save screenshots for a user and not save them for another. The screenshots currently found in the RetroArch folder at the time of the user's creation will be copied over to the new user, but not for the one you decided to not save screenshots. If you were to take screenshots with the second user, none of those will be saved. When you set as active any other user, the screenshots folder for the user that chose not to save them will be deleted. The help button in the program gives a rough of explanation of what everything does so you don't get caught with your pants down. I'd recommend to set up as "DEFAULT" user that saves every config before creating your own.

# What is being saved on each user?
Currently, the following folders and files will be saved on each user:

 * config (contains remaps)
 * saves (contains savefiles)
 * screenshots (contains screenshots)
 * states (contains savestates)
 * retroarch.cfg (contains the general config of the whole program)
 * retroarch-core-options.cfg (contains specific configuration for each core)

# Can I choose what to save on each user?
Yes, you can choose to save any combination of the above mentioned files and folders. Be careful with this feature tho, improper use may lead to data loss.

# Disclaimer
Not understanding the proper functionality of the program may lead to data loss. Please fully understand how everything works before interacting with it. I'm not responsible for any mishaps.


Thanks for using this program.

You are free to modify and distribute this software as long as you don't claim it as your own.
