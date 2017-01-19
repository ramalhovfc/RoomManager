from google.appengine.ext import ndb

class CheckRoom(ndb.Model):
	userid = ndb.IntegerProperty(repeated=True)
	roomid = ndb.IntegerProperty()
