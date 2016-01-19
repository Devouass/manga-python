import json
import os
import argparse
from utils import Logger
from downloader import Downloader
from utils import JsonFileWrapper


class MainClass:
	
	CONFIG_BASE_DIRECTORY = "config/"
	CONFIG_FORMAT = ".json"

	def __init__(self):
		self._logger = Logger.getLogger()

	def printResult(result, name):
		if result:
			self._logger.info("{} : download success".format(name))
		else:
			self._logger.warn("{} : nothing to download\n".format(name))

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
						self._logger.error("can not apply config changes, no chapter specified with -c option")
				else:
					self._logger.error("file {} does not exists".format(args.name))
			else:
				self._logger.error("can not apply config changes, no manga specified with -n option")			
		return canApply

	def updateConfigFile(self, args):
		if self._argsAreValidForUpdate(args):
			jfw = JsonFileWrapper(self._getConfigFilePath(args.name))
			actualChapter = jfw.getKey(JsonFileWrapper.CHAPTER)
			if actualChapter is not None:
				self._logger.info("update config for {}, set chapter from {} to {}".format(args.name, actualChapter, args.chapter))
				jfw.update(JsonFileWrapper.CHAPTER, str(args.chapter))
				jfw.save()
			else:
				self._logger.error("can not set chapter {} for manga {} : actual chapter is {}"\
				.format(args.chapter, args.name, actualChapter))

	def showConfigFile(self):
		for f in os.listdir(MainClass.CONFIG_BASE_DIRECTORY):
			try:
				self._logger.info(JsonFileWrapper(MainClass.CONFIG_BASE_DIRECTORY + f))
			except IOError as e:
				self._logger.error(e)

def chooseAccordingToArgs(args):
	if args.info:
		MainClass().showConfigFile()

	elif args.update:
		MainClass().updateConfigFile(args)

	else:
		downloader = Downloader()
		if args.name == "All":
			for configFile in os.listdir("config/"):
				res = downloader.download("config/" + configFile)
				printResult(res, configFile.split(".")[0])
		else:
			res = downloader.download("config/" + args.name + ".json")
			printResult(res, args.name)

def run():
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

	#deal with downloader
	if args is not None:
		chooseAccordingToArgs(args)
	else:
		Logger.getLogger().error("No args given!!")

	Logger.getLogger().close()

if __name__ == '__main__':
	run()