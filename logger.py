import sys

class Logger:
	""" logger """
	modes = ["ERROR", "INFO ", "DEBUG"]

	def __init__(self, logInFile=False):

		self.logInFile = False
		self.isFileOpen = False
		if type(logInFile) is bool:
			self.logInFile = logInFile

	def setMode(self, mode="INFO "):
		if mode in Logger.modes :
			self.mode = mode
		else :
			self.mode = Logger.modes[0]

		self.info("class Logger : logger's mode is "+self.mode)

	def debug(self, message):
		self._log(message, Logger.modes[2])

	def info(self, message):
		self._log(message, Logger.modes[1])

	def error(self, message):
		self._log(message, Logger.modes[0])

	def printSameLine(self, message, lastMessage=False):
		print(message, end="")
		if lastMessage:
			print("")
		sys.stdout.flush()

	def _log(self, message, mode):
		if mode in Logger.modes and Logger.modes.index(mode) <= Logger.modes.index(self.mode):
			if self.logInFile:
				self._printInFile("{} : {}".format(mode, message), mode)
			else :
				print("{} : {}".format(mode, message))
				sys.stdout.flush()

	def _printInFile(self, message, mode):
		print("Should be logged in a file")
		print("{} : {}".format(mode, message))

	def close(self):
		if self.logInFile and self.isFileOpen:
			print("should close the log file")