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
import queue
import threading

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


def makedir(faultyDir, folderName):

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


def checkForFaulty(path, fileName, folderName):
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
	totalTime.append(round(time.time() - startTime, 4))
	return round(time.time() - startTime, 4)
			

faultyDir = "faulty"
def getPictures(top, folderName):
	count = 1
	for submission in top:

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
				checkForFaulty(pathToFile, fileName, folderName)
				print("{}/{} t:{}s  File downloaded: {}".format(count, amountOfPictures,getTime(startTime), fileName))		
				
		except Exception as e:
			print("{}/{} Failed: {}  Reason: {}".format(count, amountOfPictures, submission.url, e))

		count += 1

def main():

	global subreddit, amountOfPictures, totalTime, q, threads


	def runIndividual(queueitem):

			subreddit = queueitem[0]
			subredditObj = reddit.subreddit(subreddit)
			top = subredditObj.top(limit=amountOfPictures)

			makedir(faultyDir, queueitem[1])
			getPictures(top, queueitem[1])

			sys.exit()


	reddit = getAuth()
	totalTime = []
	threads = []
	q = queue.Queue()
	

	if(sys.argv[1][-4:] == ".txt" and sys.argv[1] != "logindata.txt" and sys.argv[1] != "samplelogindata.txt"):
		subreddits, amountOfPictures = getArgv(True)
		for item in subreddits:
			q.put([item, str(item)])

		while not q.empty():
			t = threading.Thread(target=runIndividual, args=(q.get(),))
			threads.append(t)
			t.start()
			print("Started new thread! [{}/3]".format(len(threads)))
			
		started_threads = len(threads)
		killed_threads_count = 0
		killed_threads = []

		while(killed_threads_count < started_threads):
			for i in range(len(threads)):
				if(not threads[i].isAlive() and threads[i] not in killed_threads):
					killed_threads.append(threads[i])
					killed_threads_count += 1
			time.sleep(2)

		print("Complete! Took: {} seconds".format(round(sum(totalTime), 1)))
		exit()


	else:
		subreddit, folderName, amountOfPictures = getArgv(False)
		runIndividual([subreddit, folderName])
		print("Complete! Took: {} seconds".format(round(sum(totalTime), 1)))
		exit()

if __name__ == '__main__':
	main()