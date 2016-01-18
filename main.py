import json
import os
import argparse
import logger
from downloader import Downloader

def printResult(result, name):
	if result:
		logger.getLogger().info("{} : download success".format(name))
	else:
		logger.getLogger().warn("{} : nothing to download".format(name))
	print()

def isJsonValid(dataJson):
	isValid = False
	if dataJson is not None:
		if "name" in dataJson:
			if "url" in dataJson:
				if "chapter" in dataJson:
					isValid = True
	return isValid

def canApplyConfigChanges(args):
	canApply = False
	if args is not None:
		if args.name is not None:
			if os.path.exists("config/" + args.name + ".json"):
				if args.chapter is not None and isinstance(args.chapter, int) and int(args.chapter) >= 0:
					canApply = True
				else:
					logger.getLogger().error("can not apply config changes, no chapter specified with -c option")
			else:
				logger.getLogger().error("file {} does not exists".format("config/"+args.name))
		else:
			logger.getLogger().error("can not apply config changes, no manga specified with -n option")			
	return canApply

def chooseAccordingToArgs(args):
	if args.info:
		for configFile in os.listdir("config/"):
			data = {}
			with open("config/" + configFile, "r") as f:
				data = json.load(f)
				if isJsonValid(data):
					logger.getLogger().info("manga {} downloaded until chapter {}"\
						.format(data["name"], 0 if int(data["chapter"]) <= 0 else int(data["chapter"]) -1))

	elif args.update:
		logger.getLogger().debug("try to update configuration file")
		if canApplyConfigChanges(args):
			logger.getLogger.debug("applying changes")

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

	logger.getLogger().setMode( "DEBUG" if args.verbose else "INFO ")


	#deal with downloader
	chooseAccordingToArgs(args)

	logger.getLogger().close()

if __name__ == '__main__':
	run()