import sys

#def singleton(cls):
#	instances = {}
#	def getInstance(*args, **kwargs):
#		if cls not in instances:
#			instances[cls] = cls(*args, **kwargs)
#		return instances[cls]
#	return getInstance

#def getLogger():
#	return Logger.getLogger()

class Logger:
	""" logger """

	_logger = None

	@staticmethod
	def getLogger():
		if Logger._logger is None:
			Logger._logger = Logger()
		return Logger._logger

	def __init__(self):
		self.mute = False
		self.logInFile = False
		self.isFileOpen = False
		self.mode = "INFO "
		self.modes = ["ERROR", "WARN ", "INFO ", "DEBUG"]

	def setMute(self, mute=True):
		self.mute = mute

	def setMode(self, mode="INFO "):
		if mode in self.modes :
			self.mode = mode
		else :
			self.mode = self.modes[0]

		self.debug("class Logger : logger's mode is "+self.mode)
		print()

	def debug(self, message):
		self._log(message, self.modes[3])

	def info(self, message):
		self._log(message, self.modes[2])

	def warn(self, message):
		self._log(message, self.modes[1])

	def error(self, message):
		self._log(message, self.modes[0])

	def printSameLine(self, message, lastMessage=False):
		print(message, end="")
		if lastMessage:
			print("")
		sys.stdout.flush()

	def _log(self, message, mode):
		if not self.mute and mode in self.modes and self.modes.index(mode) <= self.modes.index(self.mode):
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