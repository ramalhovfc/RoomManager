from google.appengine.ext import ndb

class User(ndb.Model):
	username = ndb.StringProperty()
	userId = ndb.IntegerProperty()
	checked_in = ndb.BooleanProperty()
