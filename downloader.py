import json
from utils import Logger, Requester, JsonFileWrapper

class Downloader:

	def __init__(self):
		self.logger = Logger.getLogger()

	def download(self, pathToConfigFile=None):
		if pathToConfigFile is not None:
			try:
				downloadSuccess = False
				jfw = JsonFileWrapper(pathToConfigFile)
				dataAsJson = jfw.getJson()
				if self._checkJsonInput(dataAsJson):
					self._log("download {} from chapter {}".format(dataAsJson["name"], dataAsJson["chapter"]), "INFO")
					chapterAsString = dataAsJson["chapter"]
					name = dataAsJson["name"]
					url = dataAsJson["url"]
					suffixes = None
					try:
						suffixes = dataAsJson["suffixe"]
					except KeyError as e:
						self._log("no suffixe for {}".format(dataAsJson["name"]), "DEBUG")
					lastDownloadedChapter = self._startDownloading(name, url, chapterAsString, suffixes)
					if lastDownloadedChapter is not None and lastDownloadedChapter > int(dataAsJson["chapter"]):
						downloadSuccess = True

				if downloadSuccess:
					jfw.update("chapter", str(lastDownloadedChapter))
					jfw.save()

			except IOError as e:
				self._log(e, "ERROR")
		else:
			self._log("config file path is not set !!", "ERROR")

	def _startDownloading(self, name, url, chapter, suffixes):
		requester = Requester()
		lastDownloadedChapter = requester.download(name, url, chapter, suffixes)
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

	def _log(self, message, mode=""):
		if self.logger is not None:
			if mode == "ERROR":
				self.logger.error("class {} : {}".format(self.__class__.__name__, message))
			elif mode == "DEBUG":
				self.logger.debug("class {} : {}".format(self.__class__.__name__, message))
			else:
				self.logger.info("class {} : {}".format(self.__class__.__name__, message))
