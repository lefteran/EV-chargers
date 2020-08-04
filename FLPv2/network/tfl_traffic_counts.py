import urllib.request
import os
import datetime
import requests
from time import time
from pathlib import Path
import trafficCsvToJson


def exists(path):
	r = requests.head(path)
	return r.status_code == requests.codes.ok

def downloadTims():
	print("Checking for new traffic data to download ...")
	now = datetime.datetime.now()
	dateNow = now.strftime("%d%m%Y-%H%M%S")
	day = now.strftime("%d")
	timeInterval = 1200						# in seconds
	for pastSeconds in range(timeInterval):
		pastSeconds *= (-1)
		past = now + datetime.timedelta(seconds=pastSeconds)
		datePast = past.strftime("%d%m%Y-%H%M%S")
		fileName = "detdata" + past.strftime("%d%m%Y-%H%M%S") + ".csv"
		website = "http://roads.data.tfl.gov.uk/TIMS/"
		url = website + fileName
		filePath = "d:\\Github\\Exhibition-Road-Festival\\pythonScript\\traffic2806" + "\\" + fileName
		currentPath = "d:\\Github\\Exhibition-Road-Festival\\pythonScript\\traffic" + day + "06" + "\\" + fileName
		existingfile = os.path.isfile(currentPath)
		if exists(url) and not  existingfile:
			urllib.request.urlretrieve(url, filePath)
			print("File %s downloaded" %fileName)
			return filePath




def download_traffic_data():
	timsFolder = "./pythonScript/TIMS"
	if not os.path.exists(timsFolder):
		os.makedirs(timsFolder)








