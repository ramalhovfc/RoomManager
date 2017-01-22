from google.appengine.ext import ndb

# class that represents a room and the users that checked it in
class CheckRoom(ndb.Model):
	userid = ndb.IntegerProperty(repeated=True) # list of userids
	roomid = ndb.IntegerProperty()
	roomname = ndb.StringProperty()

	def saveToCloud(self):
		self.put()
