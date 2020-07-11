# Retroarch User Changer
RetroArch, now for the whole family.

# What?
RetroArch User Changer is a simple program that lets you have multiple users in RetroArch. With its easy to use interface, you will be able to add users and swap their saves or configurations automatically in miliseconds. You will be able to have multiple separate menu configurations, RetroAchievements accounts, saves and savestates, screenshots and whatever else, each user with its own.

# How?
So, how does this work? Really simple. When you create an user, the configuration on the RetroArch folder will be copied over to that new user. You can create as many as you want. At this point, you should choose an user to set as active. When a user is set as active, the configuration on RetroArch gets copied over to the previously active user (unless there's no previous active user). Then, the configuration on RetroArch gets deleted and replaced with the one found on the new active user. So now, the next time you open RetroArch, you will find the configuration of the user you've set as active. Deleting a user will delete all of its configuration and save files. You have been warned.

# Could I risk losing save files?
I tested the program a lot trying to break it and fixing the bugs that popped up. I'm confident enough that the risk of data loss should be minimal or non existent as long as you don't modify the configuration file and let the program handle it. Also, before doing anything, set up the correct RetroArch directory as there's currently no check to make sure it's a valid one and the program will start operating on whatever you provide it.

# What is being saved on each user?
Currently, the following folders and files will be saved on each user:

 * config (contains remaps)
 * saves (contains savefiles)
 * screenshots (contains screenshots)
 * states (contains savestates)
 * retroarch.cfg (contains the general config of the whole program)
 * retroarch-core-options.cfg (contains specific configuration for each core)

# Can I choose what to save on each user?
Currently, no. I'm trying to figure out a way to let users decide what to save, but this isn't supported yet. These are the files and folders that will be saved and you can't change it (unless you modify the code).

# Disclaimer
While the risk of data loss is low or non-existent, there may be an exception I haven't caught or whatever. I still need more people using the program to have a better sense of its reliability. In the case you do lose files, don't hold me accountble for it. Make backups before trying it.


You are free to modify and distribute this software as long as you don't claim it as your own.
