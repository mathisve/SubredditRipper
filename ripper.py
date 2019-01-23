#Mathis Van Eetvelde 1/16/2019
#
#
import praw, requests, re
import urllib
import time
import sys
import os
from PIL import Image
import shutil

try:
	amountOfPictures = int(sys.argv[3])
except:
	amountOfPictures = 100



file = open('logindata.txt', 'r')
logindata = []
for lines in file:
	logindata.append(lines[:-1])

reddit = praw.Reddit(client_id=logindata[0],
				     client_secret=logindata[1],
					 username=logindata[2],
					 password=logindata[3],
					 user_agent=logindata[4])

subreddit = reddit.subreddit(sys.argv[1])

top = subreddit.top(limit=amountOfPictures)

faultyDir = "faulty"
def makedir():

	try:
		if(os.path.isdir(sys.argv[2]) == True):
			print("{} directory allready exists, skipping this step!".format(sys.argv[2]))
			pass
		else:
			print("Making new directory: ", sys.argv[2])
			os.mkdir(sys.argv[2])
	except Exception as e:
		print(e)
		exit()
		
	
	try:
		if(os.path.isdir(os.path.join(sys.argv[2], faultyDir)) == True):
			print("Faulty directory allready exists, skipping this step!")
		else:
			os.mkdir(os.path.join(sys.argv[2], faultyDir))
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
		if(os.path.isfile(os.path.join(os.getcwd(), sys.argv[2], faultyDir, fileName))):
			os.remove(path)
		else:
			shutil.move(path, os.path.join(sys.argv[2], faultyDir))

	try:
		img = Image.open(path)
		imgSize = img.size
		img.close()

		if(imgSize == getFaultyImgSize()):						
			moveOrRemove(path)
	except Exception as e: 
		moveOrRemove(path)

totalTime = []
def getTime(startTime):
	stopTime = time.time()
	takenTime = stopTime - startTime
	totalTime.append(takenTime)
	return takenTime
			
makedir()

count = 0
for submission in top:
	
	count += 1
	startTime = time.time()
	try:
		title = submission.title
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

		pathToFile = os.path.join(os.getcwd(), sys.argv[2], fileName)	

		exists = False
		if(os.path.isfile(pathToFile) == True or os.path.isfile(os.path.join(os.getcwd(), sys.argv[2], faultyDir, fileName)) == True):
			exists = True

			


		if(exists == True):
			print("{}/{} t:{}s  File allready exists: {}".format(count, amountOfPictures,round(getTime(startTime), 3),fileName))
		else:
			time.sleep(.05)
			urllib.request.urlretrieve(submission.url, pathToFile)
			checkForFaulty(pathToFile, fileName)
			print("{}/{} t:{}s  File downloaded: {}".format(count, amountOfPictures,round(getTime(startTime), 3), fileName))		
			
	except Exception as e:
		print("{}/{} Failed: {}  Reason: {}".format(count, amountOfPictures, submission.url, e))

sumOfTime = 0.0
for t in totalTime:
	sumOfTime += t
print("Complete! Took: {} seconds".format(round(sumOfTime, 5)))