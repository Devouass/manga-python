import requests
import shutil
import time
from .logger import Logger
from .filemanager import FileManager

class Requester:

	DOWNLOAD_DIR = "download"

	def __init__(self):
		self.logger = Logger.getLogger()
		self.fileManager  = FileManager.getFileManager()
		if not self.fileManager.exists(Requester.DOWNLOAD_DIR):
			self._log("directory {} does not exists, create it".format(Requester.DOWNLOAD_DIR))
			self.fileManager.createDirectory(Requester.DOWNLOAD_DIR)

	def download(self, name, url, chapter):
		self._log("download {} from {}, starting chapter {} and store at {}/{}".format(name, url, chapter, Requester.DOWNLOAD_DIR, name), "DEBUG")
		self._createDirectory(Requester.DOWNLOAD_DIR, name)

		downloadDirectory = Requester.DOWNLOAD_DIR + "/" + name

		self._createDirectory(downloadDirectory, str(chapter))
		actualDownloadChapter = int(chapter)
		downloadSuccess = True
		while downloadSuccess:
			res = self._downloadAChapter(downloadDirectory, url, actualDownloadChapter)
			if res:
				self._log("chapter {} downloaded".format(actualDownloadChapter), "INFO")
				actualDownloadChapter += 1
				self._createDirectory(downloadDirectory, str(actualDownloadChapter))
			else:
				self.fileManager.deleteDirectory(downloadDirectory + "/" +str(actualDownloadChapter))
				downloadSuccess = False
		return actualDownloadChapter

	def _downloadAChapter(self, pathToStore, url, chapter):
		pageNumber = 0
		baseImageUrl = url + "/" + str(chapter) + "/"
		basePathToStore = pathToStore + "/" + str(chapter) + "/"

		nextImage = True
		downloadSuccess = False
		self._log("downloading chapter {} :".format(chapter), "INFO")
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
			if not self.fileManager.exists(basePath):
				self._log("create {}".format(basePath), "DEBUG")
				self.fileManager.createDirectory(basePath)

			newDirectory = basePath + "/" + str(name)
			if not self.fileManager.exists(newDirectory):
				self._log("create {}".format(newDirectory), "DEBUG")
				self.fileManager.createDirectory(newDirectory)

	def _log(self, message, mode=""):
		if self.logger is not None:
			if mode == "ERROR":
				self.logger.error("class {} : {}".format(self.__class__.__name__, message))
			elif mode == "DEBUG":
				self.logger.debug("class {} : {}".format(self.__class__.__name__, message))
			else:
				self.logger.info("class {} : {}".format(self.__class__.__name__, message))