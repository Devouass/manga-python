import os
import shutil
from .logger import Logger

class FileManager:

	_fm = None

	DOWNLOAD_DIR = "download/"

	@staticmethod
	def getFileManager():
		if FileManager._fm is None:
			FileManager._fm = FileManager()
		return FileManager._fm

	def __init__(self):
		self._logger = Logger.getLogger()

	def exists(self, directory):
		if directory is not None:
			return os.path.exists(directory)
		return False

	def createDirectory(self, directory):
		if directory is not None:
			if not self.exists(directory):
				os.makedirs(directory)
			else:
				self._logger.warn(self._getFormattedLog("directory {} already exists".format(directory)))
		else:
			self._logger.error((self._getFormattedLog("can not create \"None\" directory")))

	def deleteDirectory(self, directory):
		if directory is not None:
			if self.exists(directory):
				shutil.rmtree(directory)
			else:
				self._logger.warn(self._getFormattedLog("directory {} not exists".format(directory)))
		else:
			self._logger.error((self._getFormattedLog("can not delete \"None\" directory")))

	def cleanMangaDirectory(self, mangaName, chapter):
		if mangaName is not None and chapter is not None:
			self._logger.debug(self._getFormattedLog("cleaning directory for {}, and for manga upper than {}".format(mangaName, chapter)))
			if self.exists(FileManager.DOWNLOAD_DIR):
				mangaDir = FileManager.DOWNLOAD_DIR + mangaName
				if self.exists(mangaDir):
					toDel = []
					c = int(chapter)
					for f in os.listdir(mangaDir):
						if int(f) >= c:
							toDel.append(f)

					for f in toDel:
						shutil.rmtree(mangaDir + "/" + f)


	def _getFormattedLog(self, message):
		return "class {} : {}".format(self.__class__.__name__, message)
