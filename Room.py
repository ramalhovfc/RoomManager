from google.appengine.ext import ndb

class Room(ndb.Model):
	roomName = ndb.StringProperty()
	roomId = ndb.IntegerProperty()

	def saveToCloud(self):
		self.put()
