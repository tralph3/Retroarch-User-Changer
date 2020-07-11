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
from distutils.dir_util import copy_tree

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
		self.renameUserButton = Button(self.bottomFrame, text="Rename", command=lambda : renameUser(selectedUser.get()))
		self.deleteUserButton = Button(self.bottomFrame, text="Delete selected user", command=lambda : deleteUser(selectedUser.get()))
		
		self.helpButton.pack(side = "top", anchor = "n")
		
		self.retroarchDirectoryLabel.pack(side = "top", anchor = "nw")
		self.retroarchDirectoryEntry.pack(side = "left", fill = "x")
		self.retroarchDirectoryButton.pack(side = "right")
		
		self.addUserButton.pack(side = "left")
		self.setUserButton.pack(side = "left")
		self.renameUserButton.pack(side = "right")
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
				if config[user]["active"] == "True":
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

def renameUser(userID):
	if userID > 0:
		def rename(newName):
			config.set("User." + str(userID), "name", newName)
			with open("config.cfg", "w") as configFile:
				config.write(configFile)
			refreshConfigFile()
			renameUserWindow.destroy()
			mainWindow.buildUsers()

		mainWindow.launchSubWindow()
		renameUserWindow = mainWindow.subWindow
		renameUserWindow.title("Rename User")
		renameUserWindow.resizable(width = False, height = False)
		
		mainFrame = Frame(renameUserWindow, padx = 20, pady = 20)
		nameLabel = Label(mainFrame, text="New username:")
		nameEntry = Entry(mainFrame)
		addUserButton = Button(mainFrame, text="Rename...", command=lambda : rename(nameEntry.get()))

		nameLabel.pack(side = "top", anchor = "nw")
		nameEntry.pack(side = "top", anchor = "nw")
		addUserButton.pack(side = "bottom", anchor = "s")
		mainFrame.pack()

def swapFiles(newActiveUserID, prevActiveUserID=None):
		global filesToCopy

		newActiveUserDirectory = "userID_" + str(newActiveUserID)

		if prevActiveUserID is not None:
			prevActiveUserDirectory = "userID_" + str(prevActiveUserID)
		else:
			prevActiveUserDirectory = None
		retroarchDirectory = mainWindow.getRetroarchDirectory()
		
		#Copy files from retroarch to the previous active user
		if prevActiveUserDirectory is not None:
			for file in filesToCopy:
				if os.path.isdir(os.path.join(retroarchDirectory, file)):
					copy_tree(os.path.join(retroarchDirectory, file), os.path.join(prevActiveUserDirectory, file))
				else:
					shutil.copy(os.path.join(retroarchDirectory, file), os.path.join(prevActiveUserDirectory, file))

		#Remove files and folders from retroarch directory
		for file in filesToCopy:
			if os.path.isdir(os.path.join(retroarchDirectory, file)):
				shutil.rmtree(os.path.join(retroarchDirectory, file))
			else:
				os.remove(os.path.join(retroarchDirectory, file))

		#Copy files from new active user to retroarch
		for file in filesToCopy:
			if os.path.isdir(os.path.join(newActiveUserDirectory, file)):
				shutil.copytree(os.path.join(newActiveUserDirectory, file), os.path.join(retroarchDirectory, file))
			else:
				shutil.copy(os.path.join(newActiveUserDirectory, file), os.path.join(retroarchDirectory, file))

def setAsActive(newUserID, prevUserID=None):
	global userList
	if newUserID > 0:
		for user in config:
			if config.has_option(user, "active"):
				if config[user]["active"] == "True":
					prevUserID = config[user]["id"]
				config.set(user, "active", False)

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


* Put this program on a folder of its own, it will create sub-directori\
es and it's going to be messy if you leave it anywhere.

* New users will get the current configuration found on the RetroArch d\
irectory as default.

* When you set a user as active, the configuration on the RetroArch fol\
der will be copied over to the user who used to be active (this is skip\
ped if there's no previous active user). Then, the configuration in Ret\
roArch is deleted, and the configuration of the new active user is copi\
ed over to the RetroArch folder.

* Deleting a user will delete all of its configuration. This cannot be \
reverted!

* Do not manually modify the config file! You could cause data loss!


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

def createAddUserWindow():
	global userList
	global filesToCopy
	
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
			config.set(section, "active", False)

			with open("config.cfg", "w") as configFile:
				config.write(configFile)
			refreshConfigFile()
			
			os.mkdir(directory)
			
			retroarchDirectory = mainWindow.getRetroarchDirectory()

			for file in filesToCopy:
				if os.path.isdir(os.path.join(retroarchDirectory, file)):
					shutil.copytree(os.path.join(retroarchDirectory, file), os.path.join(directory, file))
				else:
					shutil.copy(os.path.join(retroarchDirectory, file), os.path.join(directory, file))

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
	addUserButton = Button(mainFrame, text="Add...", command=lambda : addCloseAndWrite(nameEntry.get()))

	nameLabel.pack(side = "top", anchor = "nw")
	nameEntry.pack(side = "top", anchor = "nw")
	addUserButton.pack(side = "bottom", anchor = "s")
	mainFrame.pack()

currentFileDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(currentFileDir)

userList = []
filesToCopy = ["retroarch.cfg", "retroarch-core-options.cfg", "saves", "states", "config", "screenshots"]

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
