#Author: Mathis Van Eetvelde 
#Github: Mathisco-01
#Started on: 1/16/2019
#

import praw
import urllib
import time
import sys
import os
from PIL import Image
import shutil

def getAuth():
	file = open('logindata.txt', 'r')
	logindata = []
	for line in file:
		logindata += line.split(",")

	for x in range(len(logindata)):
		logindata[x] = logindata[x].replace(",", "")
		
		if(logindata[x] == ""):
			del logindata[x]

	return  praw.Reddit(client_id=logindata[0],
					     client_secret=logindata[1],
						 username=logindata[2],
						 password=logindata[3],
						 user_agent=logindata[4])

def getArgv(isFile):

    
	if(isFile == False):
		def getSubreddit():
			subreddit = sys.argv[1]
			try:
				subreddit = int(subreddit)
				print("Entered subreddit (first argument) is not valid!")
				exit()
			except (TypeError, ValueError):
				return subreddit

		def getFolderName():
			folder = sys.argv[2]
			try:
				folder = int(folder)
				print("Entered folderName (second argument) is not valid!")
				exit()	
			except (TypeError, ValueError):
				return folder

		def getAmountOfPictures():
			try:
				amountOfPictures = int(sys.argv[3])
				return amountOfPictures 
			except:
				print("No Amount Of Pictures (third argument) found, using 100 as default!")
				return 100

		return getSubreddit(), getFolderName(), getAmountOfPictures()

	elif(isFile == True):

		def getSubreddits():
			filename = sys.argv[1]
			subreddits = []
			with open(filename, 'r') as subredditFile:
				for line in subredditFile:
					if(line[-1:]=="\n"):
						subreddits.append(line[:-1])
					else:
						subreddits.append(line)

			return subreddits

		def getAmountOfPictures():
			try:
				amountOfPictures = int(sys.argv[2])
				return amountOfPictures 
			except:
				print("No Amount Of Pictures (second argument) found, using 100 as default!")
				return 100

		return getSubreddits(), getAmountOfPictures()


def makedir(faultyDir):

	try:
		if(os.path.isdir(folderName) == True):
			print("{} directory allready exists, skipping this step!".format(folderName))
			pass
		else:
			print("Making new directory: ", folderName)
			os.mkdir(folderName)
	except Exception as e:
		print(e)
		exit()
		
	
	try:
		if(os.path.isdir(os.path.join(folderName, faultyDir)) == True):
			print("Faulty directory allready exists, skipping this step!")
		else:
			os.mkdir(os.path.join(folderName, faultyDir))
	except Exception as e:
		print(e)
		exit()

def getFaultyImgSize():
	img = Image.open("imgurfaulty.jpg")
	return img.size


def checkForFaulty(path, fileName):
	#checks if image size is equal to the default imgur "not available" picture
	#if so, it will move image to faulty!
	#also if the image is unopenable, it will too!

	def moveOrRemove(path):
		if(os.path.isfile(os.path.join(os.getcwd(), folderName, faultyDir, fileName))):
			os.remove(path)
		else:
			shutil.move(path, os.path.join(folderName, faultyDir))

	try:
		img = Image.open(path)
		imgSize = img.size
		img.close()

		if(imgSize == getFaultyImgSize()):						
			moveOrRemove(path)
	except Exception as e: 
		moveOrRemove(path)

def getTime(startTime):
	totalTime.append(round(time.time() - startTime, 3))
	return round(time.time() - startTime, 3)
			

faultyDir = "faulty"
def getPictures(top):
	count = 0
	for submission in top:
		
		count += 1
		startTime = time.time()
		
		try:
			title = submission.title
			#tile.strip()
			for char in [" ", ".", "!", "?", "/", "*", "[", "]", '"',":",")","(",","]:
				title = title.replace(char, "_")
			
			title = title.encode("utf-8")
			endOfUrl = submission.url[-4:]	

			if(endOfUrl == ".png" or endOfUrl == ".jpg" or endOfUrl == ".gif" ):
				fileFormat = submission.url[-4:]
			elif(submission.url[-5:] == ".JPEG" or submission.url[-5:] == ".gifv"):
				fileFormat = submission.url[-5:]
			else:
				fileFormat = ".png"

			fileName = title.decode() + fileFormat

			pathToFile = os.path.join(os.getcwd(), folderName, fileName)	

			exists = False
			if(os.path.isfile(pathToFile) == True or os.path.isfile(os.path.join(os.getcwd(), folderName, faultyDir, fileName)) == True):
				exists = True

			if(exists == True):
				print("{}/{} t:{}s  File allready exists: {}".format(count, amountOfPictures,getTime(startTime),fileName))
			else:
				time.sleep(.05)
				urllib.request.urlretrieve(submission.url, pathToFile)
				checkForFaulty(pathToFile, fileName)
				print("{}/{} t:{}s  File downloaded: {}".format(count, amountOfPictures,getTime(startTime), fileName))		
				
		except Exception as e:
			print("{}/{} Failed: {}  Reason: {}".format(count, amountOfPictures, submission.url, e))


def main():

	global subreddit, folderName, amountOfPictures, totalTime 

	def runIndividual(subreddit):

			subredditObj = reddit.subreddit(subreddit)
			top = subredditObj.top(limit=amountOfPictures)

			makedir(faultyDir)
			getPictures(top)

			print("Complete! Took: {} seconds".format(sum(totalTime)))


	reddit = getAuth()
	totalTime = []

	

	if(sys.argv[1][-4:] == ".txt" and sys.argv[1] != "logindata.txt" and sys.argv[1] != "samplelogindata.txt"):
		subreddits, amountOfPictures = getArgv(True)
		for item in subreddits:
			folderName = str(item)
			runIndividual(item)

	else:
		subreddit, folderName, amountOfPictures = getArgv(False)
		runIndividual(subreddit)

if __name__ == '__main__':
	main()