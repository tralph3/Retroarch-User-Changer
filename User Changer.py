#!/usr/bin/env python3
##################################
#                                #
#       Created by tralph3       #
#   https://github.com/tralph3   #
#                                #
##################################

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import configparser
import os
import shutil

class User:
	def __init__(self, name, ID):
		self.name = name
		self.entry = Radiobutton(mainWindow.middleFrame, text=self.name, variable=selectedUser, value=ID)
		self.ID = int(ID)

class MainWindow:
	def __init__(self, title):
		global config
		
		self.window = Tk()
		self.window.title(title)
		self.window.resizable(width = False, height = False)
		
		self.topFrame = Frame(self.window, padx = 20, pady = 20)
		self.middleFrame = Frame(self.window, padx = 20)
		self.bottomFrame = Frame(self.window, padx = 20, pady = 10)
		
		self.helpButton = Button(self.topFrame, text="Help!", command=createHelpWindow)

		self.retroarchDirectoryLabel = Label(self.topFrame, text="RetroArch directory:")
		self.retroarchDirectoryEntry = Entry(self.topFrame, width = 50, borderwidth = 2, disabledbackground="#FFFFFF", disabledforeground="#000000")

		if(config["Retroarch"]["directory"] == ""):
			self.retroarchDirectoryEntry.insert(0, "Enter RetroArch directory")
			self.retroarchDirectoryEntry.config(state="disabled")
			messagebox.showinfo(title="Attention!", message="Before doing anything, enter the RetroArch directory. You will probably make a mess if you don't.", icon="info")
		else:
			self.retroarchDirectoryEntry.insert(0, config["Retroarch"]["directory"])
			self.retroarchDirectoryEntry.config(state="disabled")

		self.retroarchDirectoryButton = Button(self.topFrame, text="...", command=lambda : askDirectory(self.retroarchDirectoryEntry, "Retroarch", "directory"))

		self.addUserButton = Button(self.bottomFrame, text="Add User", command=createAddUserWindow)
		self.setUserButton = Button(self.bottomFrame, text="Set as active user", command=lambda : setAsActive(selectedUser.get()))
		self.editUserButton = Button(self.bottomFrame, text="Edit", command=lambda : editUser(selectedUser.get()))
		self.deleteUserButton = Button(self.bottomFrame, text="Delete selected user", command=lambda : deleteUser(selectedUser.get()))
		
		self.helpButton.pack(side = "top", anchor = "n")
		
		self.retroarchDirectoryLabel.pack(side = "top", anchor = "nw")
		self.retroarchDirectoryEntry.pack(side = "left", fill = "x")
		self.retroarchDirectoryButton.pack(side = "right")
		
		self.addUserButton.pack(side = "left")
		self.setUserButton.pack(side = "left")
		self.editUserButton.pack(side = "right")
		self.deleteUserButton.pack(side = "right")

		self.topFrame.pack(side = "top", fill = "x")
		self.middleFrame.pack(side = "top", fill = "x")
		self.bottomFrame.pack(side = "top", fill = "x")
		
	def buildUsers(self):
		global userList
		
		for user in userList:
			user.entry.destroy()
		userList.clear()
		for user in config:
			if config.has_option(user, "ID"):
				if toBoolean(config[user]["active"]):
					addUser(config[user]["name"] + " (Active)", config[user]["id"])
					userList[len(userList) - 1].entry.select()
					continue
				addUser(config[user]["name"], config[user]["id"])
	
	def launchWindow(self):
		self.window.mainloop()
	
	def launchSubWindow(self):
		self.subWindow = Toplevel(self.window)
	
	def getRetroarchDirectory(self):
		return self.retroarchDirectoryEntry.get()

def toBoolean(string):
	if string == "True":
		return True
	elif string == "False":
		return False
	else:
		return None

def refreshConfigFile():
	global config
	global configFilePath
	
	config = configparser.RawConfigParser()
	config.read(configFilePath)

def askDirectory(entry, section, key):
	selectedDirectory = filedialog.askdirectory()
	if selectedDirectory != "":
		entry.config(state="normal")
		entry.delete(0, "end")
		entry.insert(0, selectedDirectory)
		entry.config(state="disabled")
		
		#Write the entered directory to the cfg
		config[section] = {key: entry.get()}
		with open("config.cfg", "w") as configFile:
			config.write(configFile)
		
		refreshConfigFile()
	return

def editUser(userID):
	if userID > 0:
		def edit(newName):
			newName = newName.lstrip().rstrip()
			for i in config:
				if not config.has_option(i, "name"):
					continue
				if config[i]["name"].lower() == newName.lower() and config[i]["id"] != str(userID):
					return
			if newName != "":
				userSection = "User." + str(userID)
				config.set(userSection, "name", newName)
				config.set(userSection, "config", remapsOverridesCheckVar.get())
				config.set(userSection, "saves", savesCheckVar.get())
				config.set(userSection, "states", statesCheckVar.get())
				config.set(userSection, "screenshots", screenshotsCheckVar.get())
				config.set(userSection, "retroarch.cfg", retroarchConfigCheckVar.get())
				config.set(userSection, "retroarch-core-options.cfg", retroarchCoreConfigCheckVar.get())

				with open("config.cfg", "w") as configFile:
					config.write(configFile)
				refreshConfigFile()

				createUserFolder(config[userSection]["directory"], userSection)

				editUserWindow.destroy()
				mainWindow.buildUsers()

		mainWindow.launchSubWindow()
		editUserWindow = mainWindow.subWindow
		editUserWindow.title("Edit User")
		editUserWindow.resizable(width = False, height = False)

		mainFrame = Frame(editUserWindow, padx = 20, pady = 20)
		nameLabel = Label(mainFrame, text="Change username:")
		nameEntry = Entry(mainFrame)
		nameEntry.insert(0, config.get("User." + str(userID), "name"))
		applyEditsButton = Button(mainFrame, text="Apply...", command=lambda : edit(nameEntry.get()))

		nameLabel.pack(side = "top", anchor = "nw")
		nameEntry.pack(side = "top", anchor = "nw")

		chooseLabel = Label(mainFrame, text="Choose what to store:")

		savesCheckVar = BooleanVar()
		savesCheck = Checkbutton(mainFrame, text="Save Games", variable=savesCheckVar)

		statesCheckVar = BooleanVar()
		statesCheck = Checkbutton(mainFrame, text="Save States", variable=statesCheckVar)

		retroarchConfigCheckVar = BooleanVar()
		retroarchConfigCheck = Checkbutton(mainFrame, text="RetroArch Configuration", variable=retroarchConfigCheckVar)

		retroarchCoreConfigCheckVar = BooleanVar()
		retroarchCoreConfigCheck = Checkbutton(mainFrame, text="Cores Configuration", variable=retroarchCoreConfigCheckVar)

		screenshotsCheckVar = BooleanVar()
		screenshotsCheck = Checkbutton(mainFrame, text="Screenshots", variable=screenshotsCheckVar)

		remapsOverridesCheckVar = BooleanVar()
		remapsOverridesCheck = Checkbutton(mainFrame, text="Remaps and Overrides", variable=remapsOverridesCheckVar)

		addUserButton = Button(mainFrame, text="Add...", command=lambda : addCloseAndWrite(nameEntry.get()))

		nameLabel.pack(side = "top", anchor = "nw")
		nameEntry.pack(side = "top", anchor = "nw")

		chooseLabel.pack(side = "top", anchor = "nw")
		savesCheck.pack(side = "top", anchor = "nw")
		statesCheck.pack(side = "top", anchor = "nw")
		retroarchConfigCheck.pack(side = "top", anchor = "nw")
		retroarchCoreConfigCheck.pack(side = "top", anchor = "nw")
		screenshotsCheck.pack(side = "top", anchor = "nw")
		remapsOverridesCheck.pack(side = "top", anchor = "nw")

		applyEditsButton.pack(side = "bottom", anchor = "s")
		mainFrame.pack()

def swapFiles(newUserID, prevUserID=None):
	global standardFiles
	global standardFolders

	retroarchDirectory = mainWindow.getRetroarchDirectory()

	newUserSection = "User." + str(newUserID)
	newUserFiles = []
	newUserFolders = []
	newUserDirectory = config.get(newUserSection, "directory")

	#Generate folders and files lists
	for file in standardFiles:
		if toBoolean(config.get(newUserSection, file)):
			newUserFiles.append(file)
	for folder in standardFolders:
		if toBoolean(config.get(newUserSection, folder)):
			newUserFolders.append(folder)

	#If there is a previous user
	if prevUserID is not None:
		prevUserSection = "User." + str(prevUserID)
		prevUserFiles = []
		prevUserFolders = []
		prevUserDirectory = config.get(prevUserSection, "directory")

		#Generate folders and files lists
		for file in standardFiles:
			if toBoolean(config.get(prevUserSection, file)):
				prevUserFiles.append(file)
		for folder in standardFolders:
			if toBoolean(config.get(prevUserSection, folder)):
				prevUserFolders.append(folder)

		for folder in prevUserFolders:
			#Remove folders on the previous active user directory
			shutil.rmtree(os.path.join(prevUserDirectory, folder))
			#Copy folders from retroarch directory
			shutil.copytree(os.path.join(retroarchDirectory, folder), os.path.join(prevUserDirectory, folder))

		for file in prevUserFiles:
			#Remove files from previous active user directory
			os.remove(os.path.join(prevUserDirectory, file))
			#Copy files from retroarch directory
			shutil.copy(os.path.join(retroarchDirectory, file), os.path.join(prevUserDirectory, file))

		for folder in newUserFolders:
			#Remove folders from retroarch directory
			shutil.rmtree(os.path.join(retroarchDirectory, folder))
			#Copy folders from new active user to retroarch
			shutil.copytree(os.path.join(newUserDirectory, folder), os.path.join(retroarchDirectory, folder))

		for file in newUserFiles:
			#Remove files from retroarch directory
			os.remove(os.path.join(retroarchDirectory, file))
			#Copy files from new active user to retroarch
			shutil.copy(os.path.join(newUserDirectory, file), os.path.join(retroarchDirectory, file))

	#If there's not a previous user
	else:
		for folder in newUserFolders:
			#Remove folders from retroarch directory
			shutil.rmtree(os.path.join(retroarchDirectory, folder))
			#Copy folders from new active user to retroarch
			shutil.copytree(os.path.join(newUserDirectory, folder), os.path.join(retroarchDirectory, folder))

		for file in newUserFiles:
			#Remove files from retroarch directory
			if os.path.exists(os.path.join(retroarchDirectory, file)):
				os.remove(os.path.join(retroarchDirectory, file))
			#Copy files from new active user to retroarch
			shutil.copy(os.path.join(newUserDirectory, file), os.path.join(retroarchDirectory, file))

	for folder in standardFolders:
		if not folder in newUserFolders:
			shutil.rmtree(os.path.join(retroarchDirectory, folder))
			os.mkdir(os.path.join(retroarchDirectory, folder))
	for file in standardFiles:
		if not file in newUserFiles and os.path.exists(os.path.join(retroarchDirectory, file)):
			os.remove(os.path.join(retroarchDirectory, file))
			open(os.path.join(retroarchDirectory, file), "a").close()

def setAsActive(newUserID, prevUserID=None):
	global userList
	if newUserID > 0:
		for user in config:
			if config.has_option(user, "active"):
				if toBoolean(config[user]["active"]):
					prevUserID = config[user]["id"]
					if prevUserID == newUserID:
						return
					config.set(user, "active", False)
					break

		config.set("User." + str(newUserID), "active", True)
		with open("config.cfg", "w") as configFile:
			config.write(configFile)
		refreshConfigFile()

		swapFiles(newUserID, prevUserID)
		
		mainWindow.buildUsers()

def deleteUser(userID):
	global userList

	if userID > 0:
		confirmationMessage = messagebox.askquestion("Delete User", """Are you sure?

The configurations and save files for this user will be deleted permane\
ntly, this cannot be undone.

Continue?""", icon="warning")

		if confirmationMessage == "yes":
			userToDeleteIndex = 0
			for i in userList:
				#Search for the position of the user to delete in the list
				if int(i.ID) == userID:
					#Destroy de radiobutton widget
					userList[userToDeleteIndex].entry.destroy()
					
					#Delete the directory
					shutil.rmtree(config["User." + str(userID)]["directory"], ignore_errors = True)
					
					#Delete the user object
					del userList[userToDeleteIndex]
					
					#Delete the config file section
					config.remove_section("User." + str(userID))
					
					#Write changes to config file
					with open("config.cfg", "w") as configFile:
						config.write(configFile)
					refreshConfigFile()
					
					#Rebuiil users with new modified config file
					mainWindow.buildUsers()
					break
				else:
					userToDeleteIndex += 1

def addUser(userName, ID=None):
	if(userName != ""):
		if ID == None:
			ID = assignID()
		#Create new user and add it to the list
		userList.append(User(userName, ID))
		#Pack the new user into the main window
		userList[len(userList) - 1].entry.pack(side = "top", anchor = "w")

		refreshConfigFile()

def createHelpWindow():
	mainWindow.launchSubWindow()
	helpWindow = mainWindow.subWindow
	helpWindow.title("Help")
	helpWindow.resizable(width = False, height = False)
	
	helpFrame = Frame(helpWindow, padx = 20, pady = 20)
	help = Message(helpFrame, text="""Things you should know!


* Put this program on a folder of its own, it will create sub-directory\
es and it's going to be messy if you leave it anywhere.

* New users will get the current configuration found on the RetroArch d\
irectory as default.

* When you set a user as active, the configuration on the RetroArch fol\
der will be copied over to the user who used to be active (this is skip\
ped if there's no previous active user). Then, the configuration in Ret\
roArch is deleted, and the configuration of the new active user is copi\
ed over to the RetroArch folder.

* If you choose to not store something in a user, every time you use tha\
t user the thing you chose to not store will be empty or default. (I.E, \
if you choose to not store saves every time you set that user as active \
it will have no saves).

* If you later choose to stop storing some folder or file on any user, t\
he currently stored data for those files and folders for that user will \
be deleted. If you want to store new data, the current data found in Ret\
roArch will be copied over.

* Deleting a user will delete all of its saves and configurations. This\
 cannot be reverted!

* DO NOT manually modify the config file! You could cause data loss!

* DO NOT use this program while RetroArch is open.

-----------------------------------------------

Thanks for using my program! For more, visit github.com/tralph3
""")

	helpFrame.pack()
	help.pack(side = "top")

def assignID():
	candidateID = 1
	IDList = []
	for user in config:
		if not config.has_option(user, "id"):
			continue
		IDList.append(config[user]["id"])
	while True:
		if(str(candidateID) in IDList):
			candidateID += 1
		else:
			return candidateID

def createUserFolder(directory, section):
	global standardFiles
	global standardFolders

	if not os.path.exists(directory):
		os.mkdir(directory)

	retroarchDirectory = mainWindow.getRetroarchDirectory()

	userFiles = []
	userFolders = []

	#Generate folders and files lists
	for file in standardFiles:
		if toBoolean(config.get(section, file)):
			userFiles.append(file)
	for folder in standardFolders:
		if toBoolean(config.get(section, folder)):
			userFolders.append(folder)

	for folder in userFolders:
		#Copy folders from retroarch directory
		if not os.path.exists(os.path.join(directory, folder)):
			shutil.copytree(os.path.join(retroarchDirectory, folder), os.path.join(directory, folder))


	for file in userFiles:
		#Copy files from retroarch directory
		if not os.path.exists(os.path.join(directory, file)):
			shutil.copy(os.path.join(retroarchDirectory, file), os.path.join(directory, file))

	for folder in standardFolders:
		if not folder in userFolders and os.path.exists(os.path.join(directory, folder)):
			shutil.rmtree(os.path.join(directory, folder))
	for file in standardFiles:
		if not file in userFiles and os.path.exists(os.path.join(directory, file)):
			os.remove(os.path.join(directory, file))


def createAddUserWindow():
	global userList
	global standardFiles
	global standardFolders

	def addCloseAndWrite(userName):
		userName = userName.lstrip().rstrip()
		for i in config:
			if not config.has_option(i, "name"):
				continue
			if config[i]["name"].lower() == userName.lower():
				return
		if userName != "":
			ID = assignID()
			section = "User." + str(ID)
			directory = "userID_" + str(ID)

			config.add_section(section)
			config.set(section, "name", userName)
			config.set(section, "id", ID)
			config.set(section, "directory", directory)
			config.set(section, "config", remapsOverridesCheckVar.get())
			config.set(section, "saves", savesCheckVar.get())
			config.set(section, "states", statesCheckVar.get())
			config.set(section, "screenshots", screenshotsCheckVar.get())
			config.set(section, "retroarch.cfg", retroarchConfigCheckVar.get())
			config.set(section, "retroarch-core-options.cfg", retroarchCoreConfigCheckVar.get())
			config.set(section, "active", False)

			with open("config.cfg", "w") as configFile:
				config.write(configFile)
			refreshConfigFile()

			createUserFolder(directory, section)

			addUser(userName, ID)
			addUserWindow.destroy()
	
	#Open a subwindow and add its widgets
	mainWindow.launchSubWindow()
	addUserWindow = mainWindow.subWindow
	addUserWindow.title("Add User")
	addUserWindow.resizable(width = False, height = False)
	
	mainFrame = Frame(addUserWindow, padx = 20, pady = 20)
	nameLabel = Label(mainFrame, text="User Name:")
	nameEntry = Entry(mainFrame)

	chooseLabel = Label(mainFrame, text="Choose what to store:")

	savesCheckVar = BooleanVar()
	#savesCheckVar.set(True).get()
	savesCheck = Checkbutton(mainFrame, text="Save Games", variable=savesCheckVar)

	statesCheckVar = BooleanVar()
	statesCheck = Checkbutton(mainFrame, text="Save States", variable=statesCheckVar)

	retroarchConfigCheckVar = BooleanVar()
	retroarchConfigCheck = Checkbutton(mainFrame, text="RetroArch Configuration", variable=retroarchConfigCheckVar)

	retroarchCoreConfigCheckVar = BooleanVar()
	retroarchCoreConfigCheck = Checkbutton(mainFrame, text="Cores Configuration", variable=retroarchCoreConfigCheckVar)

	screenshotsCheckVar = BooleanVar()
	screenshotsCheck = Checkbutton(mainFrame, text="Screenshots", variable=screenshotsCheckVar)

	remapsOverridesCheckVar = BooleanVar()
	remapsOverridesCheck = Checkbutton(mainFrame, text="Remaps and Overrides", variable=remapsOverridesCheckVar)

	addUserButton = Button(mainFrame, text="Add...", command=lambda : addCloseAndWrite(nameEntry.get()))

	nameLabel.pack(side = "top", anchor = "nw")
	nameEntry.pack(side = "top", anchor = "nw")

	chooseLabel.pack(side = "top", anchor = "nw")
	savesCheck.pack(side = "top", anchor = "nw")
	statesCheck.pack(side = "top", anchor = "nw")
	retroarchConfigCheck.pack(side = "top", anchor = "nw")
	retroarchCoreConfigCheck.pack(side = "top", anchor = "nw")
	screenshotsCheck.pack(side = "top", anchor = "nw")
	remapsOverridesCheck.pack(side = "top", anchor = "nw")

	addUserButton.pack(side = "bottom", anchor = "s")
	mainFrame.pack()

currentFileDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(currentFileDir)

userList = []
standardFolders = ["saves", "states", "config", "screenshots"]
standardFiles = ["retroarch.cfg", "retroarch-core-options.cfg"]

config = configparser.RawConfigParser()
configFilePath = r'config.cfg'
config.read(configFilePath)

if not os.path.isfile("config.cfg"):
	config.add_section("Retroarch")
	config.set("Retroarch", "directory", "")
	with open("config.cfg", "w") as configFile:
			config.write(configFile)
	refreshConfigFile()

mainWindow = MainWindow("tralph3's User Changer")
selectedUser = IntVar()
mainWindow.buildUsers()

mainWindow.launchWindow()
