import os
import json
from utils import Logger
from requester import Requester

class Downloader:

	downloadDirectory = "download"

	def __init__(self):
		self.logger = Logger.getLogger()
		if not os.path.exists(Downloader.downloadDirectory):
			self._log("directory {} does not exists, create it".format(Downloader.downloadDirectory))
			os.makedirs(Downloader.downloadDirectory)


	def download(self, pathToConfigFile=None):
		downloadSuccess = False
		if self._checkConfigFileInput(pathToConfigFile):
			dataAsJson = {}
			chapterAsString = ""
			with open(pathToConfigFile, 'r') as data_file:
				dataAsJson = json.load(data_file)
				if self._checkJsonInput(dataAsJson):
					self._log("download {} from chapter {}".format(dataAsJson["name"], dataAsJson["chapter"]), "INFO")
					chapterAsString = dataAsJson["chapter"]
					name = dataAsJson["name"]
					url = dataAsJson["url"]
					lastDownloadedChapter = self._startDownloading(name, url, chapterAsString)
					if lastDownloadedChapter is not None and lastDownloadedChapter > int(dataAsJson["chapter"]):
						downloadSuccess = True	
			if downloadSuccess:
				with open(pathToConfigFile, 'w') as data_file:
					dataAsJson["chapter"] = str(lastDownloadedChapter)
					data_file.write(json.dumps(dataAsJson))
		return downloadSuccess
	

	def _startDownloading(self, name, url, chapter):
		requester = Requester()
		lastDownloadedChapter = requester.download(Downloader.downloadDirectory, name, url, chapter)
		return int(lastDownloadedChapter)


	def _checkJsonInput(self, json):
		isValid = False
		if "name" in json:
			if "url" in json:
				if "chapter" in json:
					isValid = True
				else:
					self._log("config file does not contains chapter", "ERROR")
			else:
				self._log("config file does not contains url", "ERROR")
		else:
			self._log("config file does not contains name", "ERROR")
		return isValid


	def _checkConfigFileInput(self, pathToConfigFile):
		isValid = False
		if pathToConfigFile is not None:
			if os.path.exists(pathToConfigFile):
				self._log("path to config file is valid", "DEBUG")
				isValid = True
			else:
				self._log("no config for manga {} defined ".format(pathToConfigFile), "ERROR")
		else:
			self._log("no path to config file given !", "ERROR")
		return isValid


	def _log(self, message, mode=""):
		if self.logger is not None:
			if mode == "ERROR":
				self.logger.error("class {} : {}".format(self.__class__.__name__, message))
			elif mode == "DEBUG":
				self.logger.debug("class {} : {}".format(self.__class__.__name__, message))
			else:
				self.logger.info("class {} : {}".format(self.__class__.__name__, message))
