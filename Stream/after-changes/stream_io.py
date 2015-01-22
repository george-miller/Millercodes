# This file contains method used to interact with the save.txt file
# The file will be a text file containing 4 values seperated by new lines
# line number: 0 the current level
# 1 The number of lives this user has
# 2 The current highscore on this machine
# 3 The sound preference (1 for on or 0 for off)

# A method to update the file containing the current level and lives someone has
def updateFile(index,change):
	f = open("saves.txt", "r")
	lines = f.readlines()
	f.close()
	
	f = open("saves.txt","w")
	for i in range(len(lines)):
		if (i == index):
			f.write(str(change) + "\n")
		else:
			f.write(lines[i])
	f.close()

# returns the current level or # of lives
# make i = 0 for level, make i = 1 for lives
def readFile(i):
	f = open("saves.txt", "r")
	line = int(float(f.readlines()[i]))
	f.close()
	return line
