from google.appengine.ext import ndb

class CheckRoom(ndb.Model):
	userId = ndb.IntegerProperty(repeated=True)
	roomId = ndb.IntegerProperty()
