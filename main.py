import json
import os
import argparse
from logger import Logger
from downloader import Downloader

#parser arguments
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", nargs='?', const="1", default="All", type=str, help="the name of the manga to download: [ OnePiece, FairyTail, All ]")
parser.add_argument("-v", "--verbose", action="store_true", help="print debug logs")
args = parser.parse_args()

#deal with logger
logger = Logger()
logger.setMode( "DEBUG" if args.verbose else "INFO ")

def printResult(result, name):
	if result:
		logger.info("{} : download success".format(name))
	else:
		logger.warn("{} : nothing to download".format(name))
	print()

#deal with downloader
downloader = Downloader(logger)
if args.name == "All":
	for configFile in os.listdir("config/"):
		res = downloader.download("config/" + configFile)
		printResult(res, configFile.split(".")[0])
else:
	res = downloader.download("config/" + args.name + ".json")
	printResult(res, args.name)

logger.close()