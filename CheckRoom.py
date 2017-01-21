from google.appengine.ext import ndb

class CheckRoom(ndb.Model):
	userid = ndb.IntegerProperty(repeated=True)
	roomid = ndb.IntegerProperty()
	roomname = ndb.StringProperty()

	def saveToCloud(self):
		self.put()
