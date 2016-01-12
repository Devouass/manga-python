import json
import os
import argparse
from logger import Logger

#parser arguments
parser = argparse.ArgumentParser()
parser.add_argument("name", type=str, help="the name of the manga to download: [ OnePiece ]")
parser.add_argument("-v", "--verbose", action="store_true", help="print debug logs")
args = parser.parse_args()

#deal with logger
logger = Logger()
logger.setMode( "DEBUG" if args.verbose else "INFO")

configFileName = "config/" + args.name + ".json"

if os.path.exists(configFileName):
	with open('config/OnePiece.json') as data_file:    
	    data = json.load(data_file)
	    logger.debug(data)

else:
	logger.error("no config for manga {} defined ".format(args.name))

	
logger.close()