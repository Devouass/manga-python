import os


def getFileManager():
	return FileManager.getFileManager()

class FileManager:

	_fm = None

	@staticmethod
	def getFileManager():
		if FileManager._fm is None:
			FileManager._fm = FileManager()
		return FileManager._fm

	def __init__(self):


	def exists(self, directory):
		if str(directory) is not None:
			return os.path.exists(directory)
		return False