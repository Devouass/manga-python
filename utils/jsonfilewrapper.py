from .filemanager import FileManager
import json

class JsonFileWrapper:

	NAME = "name"
	URL = "url"
	CHAPTER = "chapter"
	SUFFIXE = "suffixe"

	def __init__(self, pathToFile):
		if not FileManager.getFileManager().exists(pathToFile):
			raise IOError("file does not exists: {}".format(pathToFile))
		self._path = pathToFile
		with open(self._path, "r") as f:
			self._json = json.load(f)
		if not self.isJsonValid():
			raise IOError("file {} is not valid !".format(pathToFile))

	def update(self, key, value):
		if key is not None and key in self._json:
			self._json[key] = value

	def getJson(self):
		return self._json.copy()

	def getKey(self, key):
		if key is not None and key in self._json:
			return self._json[key]
		return None

	def isJsonValid(self):
		isValid = False
		if JsonFileWrapper.NAME in self._json \
		and JsonFileWrapper.URL in self._json \
		and JsonFileWrapper.CHAPTER in self._json:
			isValid = True
		return isValid

	def __str__(self):
		return "name: {}, chapter: {}, url: {}"\
			.format(self._json[JsonFileWrapper.NAME], self._json[JsonFileWrapper.CHAPTER], self._json[JsonFileWrapper.URL])

	def save(self):
		with open(self._path, "w") as f:
			f.write(json.dumps(self._json))
