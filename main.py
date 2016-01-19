import json
import os
import argparse
from utils import Logger, JsonFileWrapper
from downloader import Downloader


class MainClass:
	
	CONFIG_BASE_DIRECTORY = "config/"
	CONFIG_FORMAT = ".json"

	def __init__(self):
		self._logger = Logger.getLogger()

	def printResult(self, result, name):
		if result:
			self._logger.info("class Main : download success\n".format(name))
		else:
			self._logger.warn("class Main : {} => nothing to download\n".format(name))

	def _getConfigFilePath(self, name):
		return MainClass.CONFIG_BASE_DIRECTORY + name + MainClass.CONFIG_FORMAT if name is not None else None

	def _argsAreValidForUpdate(self, args):
		canApply = False
		if args is not None:
			if args.name is not None:
				if os.path.exists(self._getConfigFilePath(args.name)):
					if args.chapter is not None and isinstance(args.chapter, int) and int(args.chapter) >= 1:
						canApply = True
					else:
						self._logger.error("class Main : can not apply config changes, no chapter specified with -c option")
				else:
					self._logger.error("class Main : file {} does not exists".format(args.name))
			else:
				self._logger.error("class Main : can not apply config changes, no manga specified with -n option")			
		return canApply

	def updateConfigFile(self, args):
		if self._argsAreValidForUpdate(args):
			jfw = JsonFileWrapper(self._getConfigFilePath(args.name))
			actualChapter = jfw.getKey(JsonFileWrapper.CHAPTER)
			if actualChapter is not None:
				self._logger.info("class Main : update config for {}, set chapter from {} to {}".format(args.name, actualChapter, args.chapter))
				jfw.update(JsonFileWrapper.CHAPTER, str(args.chapter))
				jfw.save()
			else:
				self._logger.error("class Main : can not set chapter {} for manga {} : actual chapter is {}"\
				.format(args.chapter, args.name, actualChapter))

	def showConfigFile(self, args):
		if args.name is not None:
			if os.path.exists(self._getConfigFilePath(args.name)):
				self._logger.info(JsonFileWrapper(self._getConfigFilePath(args.name)))
			else:
				self._logger.error("class Main : manga {} not available".format(args.name))
		else:
			for f in os.listdir(MainClass.CONFIG_BASE_DIRECTORY):
				try:
					self._logger.info(JsonFileWrapper(MainClass.CONFIG_BASE_DIRECTORY + f))
				except IOError as e:
					self._logger.error(e)

	def download(self, args):
		downloader = Downloader()
		if args.name == "All":
			for configFile in os.listdir("config/"):
				res = downloader.download("config/" + configFile)
				self.printResult(res, configFile.split(".")[0])
		else:
			res = downloader.download("config/" + args.name + ".json")
			self.printResult(res, args.name)

if __name__ == '__main__':
	#parser arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--name", nargs='?', const="1", default="All",\
		type=str, help="the name of the manga to download: [ OnePiece, FairyTail, All ], default is All")
	parser.add_argument("-v", "--verbose", action="store_true", help="print debug logs")
	parser.add_argument("-i", "--info", action="store_true", help="give infos of latest download version of each manga")
	parser.add_argument("-u", "--update", action="store_true", help="update version of manga (with -u and -n option, fail otherwise)")
	parser.add_argument("-c", "--chapter", nargs='?', const="1", default=0, type=int, help="with -u and -n option, specify the version")
	args = parser.parse_args()

	Logger.getLogger().setMode( "DEBUG" if args.verbose else "INFO ")

	if args.info:
		MainClass().showConfigFile(args)

	elif args.update:
		MainClass().updateConfigFile(args)

	else:
		MainClass().download(args)

	Logger.getLogger().close()