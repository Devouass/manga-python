import json
import os
import argparse
from logger import Logger
from downloader import Downloader

#parser arguments
parser = argparse.ArgumentParser()
parser.add_argument("name", type=str, help="the name of the manga to download: [ OnePiece ]")
parser.add_argument("-v", "--verbose", action="store_true", help="print debug logs")
args = parser.parse_args()

#deal with logger
logger = Logger()
logger.setMode( "DEBUG" if args.verbose else "INFO ")

#deal with downloader
downloader = Downloader(logger)
res = downloader.download("config/" + args.name + ".json")

if res:
	logger.info("download success")
else:
	logger.error("nothing to download")

logger.close()