import json
import requests

# Gets rooms from an external system
class SpaceFetcher:
	def __init__(self, endpoint = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces"):
		self.endpoint = endpoint

	def getSpaceById(self, roomId = ""):
		if roomId:
			pathToGet = self.endpoint + "/" + str(roomId)
		else:
			pathToGet = self.endpoint

		result = requests.get(pathToGet)
		spaces = json.loads(result.text)
		return spaces
