from google.appengine.ext import ndb

class User(ndb.Model):
	username = ndb.StringProperty()
	userid = ndb.IntegerProperty()
	checked_in = ndb.IntegerProperty()
