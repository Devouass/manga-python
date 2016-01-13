import os
import requests
import shutil
import time

class Requester:

	def __init__(self, logger=None):
		self.logger = logger

	def download(self, pathToStore, name, url, chapter):
		self._log("download {} from {}, starting chapter {} and store at {}/{}".format(name, url, chapter, pathToStore, name), "DEBUG")
		self._createDirectory(pathToStore, name)

		downloadDirectory = pathToStore + "/" + name

		self._createDirectory(downloadDirectory, str(chapter))
		actualDownloadChapter = int(chapter)
		downloadSuccess = True
		while downloadSuccess:
			res = self._downloadAChapter(downloadDirectory, url, actualDownloadChapter)
			if res:
				self._log("chapter {} downloaded".format(actualDownloadChapter), "INFO ")
				actualDownloadChapter += 1
				self._createDirectory(downloadDirectory, str(actualDownloadChapter))
			else:
				self._delDirectory(downloadDirectory, str(actualDownloadChapter))
				downloadSuccess = False
		return actualDownloadChapter


	def _downloadAChapter(self, pathToStore, url, chapter):
		pageNumber = 0
		baseImageUrl = url + "/" + str(chapter) + "/"
		basePathToStore = pathToStore + "/" + str(chapter) + "/"

		nextImage = True
		downloadSuccess = False
		self._log("downloading chapter {} :".format(chapter), "INFO ")
		while nextImage:
			pageNumberFormatted = self._formatPageNumber(pageNumber)
			imageUrl = baseImageUrl + pageNumberFormatted + ".jpg"
			self._log("try to download {}".format(imageUrl), "DEBUG")
			r = requests.get(imageUrl, stream=True)
			if r.status_code == 200:
				self._log("download page image {} from chapter {}".format(pageNumberFormatted, chapter), "DEBUG")
				self.logger.printSameLine("*")
				if not downloadSuccess:
					downloadSuccess = True
				pageNumber += 1
				imagePath =  basePathToStore + pageNumberFormatted + ".jpg"
				with open(imagePath, 'wb') as imageFile:
					r.raw.decode_content = True
					shutil.copyfileobj(r.raw, imageFile)
			else:
				if pageNumber == 0:
					pageNumber += 1
				else:
					if downloadSuccess:
						self.logger.printSameLine("",True)
					nextImage = False
		
		return downloadSuccess


	def _formatPageNumber(self, pageNumber):
		pageFormatted = ""
		if pageNumber < 10:
			pageFormatted = "0" + str(pageNumber)
		else :
			pageFormatted = str(pageNumber)
		return pageFormatted

	def _createDirectory(self, basePath, name):
		if basePath is not None and name is not None:
			if not os.path.exists(basePath):
				self._log("create {}".format(basePath), "DEBUG")
				os.makedirs(basePath)

			newDirectory = basePath + "/" + str(name)
			if not os.path.exists(newDirectory):
				self._log("create {}".format(newDirectory), "DEBUG")
				os.makedirs(newDirectory)

	def _delDirectory(self, directory, name):
		if directory is not None and name is not None:
			toDel = directory + "/" + name
			if os.path.exists(toDel):
				os.rmdir(toDel)
				self._log("delete {}".format(toDel), "DEBUG")

	def _log(self, message, mode=""):
		if self.logger is not None:
			if mode == "ERROR":
				self.logger.error("class {} : {}".format(self.__class__.__name__, message))
			elif mode == "DEBUG":
				self.logger.debug("class {} : {}".format(self.__class__.__name__, message))
			else:
				self.logger.info("class {} : {}".format(self.__class__.__name__, message))