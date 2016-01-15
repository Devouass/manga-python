import json
import os
import argparse
import logger
from downloader import Downloader

#parser arguments
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", nargs='?', const="1", default="All", type=str, help="the name of the manga to download: [ OnePiece, FairyTail, All ]")
parser.add_argument("-v", "--verbose", action="store_true", help="print debug logs")
parser.add_argument("-u", "--update", action="store_true", help="update version of manga specified with -n argument in config file")
parser.add_argument("-c", "--chapter", nargs='?', const="1", default=0, type=int, help="with -u option, give the version to store in the config file")
args = parser.parse_args()

logger.getLogger().setMode( "DEBUG" if args.verbose else "INFO ")

def printResult(result, name):
	if result:
		logger.getLogger().info("{} : download success".format(name))
	else:
		logger.getLogger().warn("{} : nothing to download".format(name))
	print()


def chooseAccordingToArgs(args):
	downloader = Downloader()
	if args.name == "All":
		for configFile in os.listdir("config/"):
			res = downloader.download("config/" + configFile)
			printResult(res, configFile.split(".")[0])
	else:
		res = downloader.download("config/" + args.name + ".json")
		printResult(res, args.name)


#deal with downloader
chooseAccordingToArgs(args)

logger.getLogger().close()