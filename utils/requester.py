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

	def download(self, name, url, chapter, suffixes):
		self._log("download {} from {}, starting chapter {} and store at {}/{}".format(name, url, chapter, Requester.DOWNLOAD_DIR, name), "DEBUG")
		self._createDirectory(Requester.DOWNLOAD_DIR, name)

		downloadDirectory = Requester.DOWNLOAD_DIR + "/" + name

		self._createDirectory(downloadDirectory, str(chapter))
		actualDownloadChapter = int(chapter)
		downloadSuccess = True
		while downloadSuccess:
			res = self._downloadAChapter(downloadDirectory, url, actualDownloadChapter, suffixes)
			if res:
				self._log("chapter {} downloaded".format(actualDownloadChapter), "INFO")
				actualDownloadChapter += 1
				self._createDirectory(downloadDirectory, str(actualDownloadChapter))
			else:
				self.fileManager.deleteDirectory(downloadDirectory + "/" +str(actualDownloadChapter))
				downloadSuccess = False
		return actualDownloadChapter

	def _downloadAChapter(self, pathToStore, url, chapter, suffixes):

		self.logger.printSameLine("", True)
		self._log("downloading chapter {} :".format(chapter), "INFO")

		chapterDownloaded = False

		basePathToStore = pathToStore + "/" + str(chapter) + "/"
		baseImageUrl = url + "/" + str(chapter) + "/"

		#first try without suffixe:
		tryUrl = True
		pageNumber = 0
		pageType = ".jpg"
		downloadSuccess = False
		self._log("try to download chapter {} without suffixe".format(chapter), "INFO")
		while tryUrl:
			imageUrl = baseImageUrl + self._formatPageNumber(pageNumber) + pageType
			imagePathStore = basePathToStore + self._formatPageNumber(pageNumber) + pageType
			downloadSuccess = self._downloadAPage(imageUrl, imagePathStore)
			if downloadSuccess:
				tryUrl = False
			else:
				self.logger.printSameLine("x")
				pageNumber += 1
				#TODO add .png
				if pageNumber > 2:
					self.logger.printSameLine("", True)
					self._log("nothing to download without suffixe for chapter {}".format(chapter), "ERROR")
					tryUrl = False

		#then try with suffixe
		if not downloadSuccess:
			if suffixes:
				i = 0
				nbSuffixes = len(suffixes)
				while i < nbSuffixes and not downloadSuccess:
					baseImageUrl = url + "/" + str(chapter) + "/" + suffixes[i] + "/"
					self._log("try to download chapter {} with suffixe {}".format(chapter, suffixes[i]), "INFO")
					self._log("try with base url = {}".format(baseImageUrl), "DEBUG")
					i += 1
					tryUrl = True
					pageNumber = 0
					while tryUrl:
						imageUrl = baseImageUrl + self._formatPageNumber(pageNumber) + pageType
						imagePathStore = basePathToStore + self._formatPageNumber(pageNumber) + pageType
						downloadSuccess = self._downloadAPage(imageUrl, imagePathStore)
						if downloadSuccess:
							tryUrl = False
						else:
							self.logger.printSameLine("x")
							pageNumber += 1
							#TODO add .png
							if pageNumber > 2:
								self.logger.printSameLine("", True)
								self._log("nothing to download with suffixe {} for chapter {}".format(suffixes[i-1], chapter), "ERROR")
								tryUrl = False

		if downloadSuccess:
			nextImageInChapter = True
			count = 0
			while nextImageInChapter:
				self.logger.printSameLine("*")
				pageNumber += 1
				imageUrl = baseImageUrl + self._formatPageNumber(pageNumber) + pageType
				imagePathStore = basePathToStore + self._formatPageNumber(pageNumber) + pageType
				nextImageInChapter = self._downloadAPage(imageUrl, imagePathStore)
				count +=1
			self.logger.printSameLine("",True)
			self._log("{} pages donwloaded for chapter {}".format(count, chapter), "INFO")
			chapterDownloaded = True

		return chapterDownloaded

	def _formatPageNumber(self, pageNumber):
		pageFormatted = ""
		if pageNumber < 10:
			pageFormatted = "0" + str(pageNumber)
		else :
			pageFormatted = str(pageNumber)
		return pageFormatted

	def _downloadAPage(self, url, storeUrl):
		self._log("try to download {}".format(url), "DEBUG")
		success = False
		r = requests.get(url, stream=True)
		if r.status_code == 200:
			self._log("download {}".format(url), "DEBUG")
			with open(storeUrl, 'wb') as imageFile:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw, imageFile)
				success = True
		return success

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
