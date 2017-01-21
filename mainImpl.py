from google.appengine.ext import ndb

from User import User
from CheckRoom import CheckRoom
from Room import Room

def signin_user_impl(username):
	max_userId = 0
	if username != "admin":
		query = User.query().fetch()
		print query
		for utilizador in query:
			print utilizador
			if utilizador.userid>max_userId:
				max_userId=utilizador.userid
			if utilizador.username == username:
				return -1
		max_userId += 1
		user_exemplo = User(username = username, userid = max_userId, checked_in = -1, key = ndb.Key(User, max_userId))
		user_exemplo.put()
		return max_userId
	else:
		user_exemplo = User(username = username, userid = 0, checked_in = -1, key = ndb.Key(User, 0))
		user_exemplo.put()
		return 0

def login_user_impl(username):
	query = User.query().fetch()
	for utilizador in query:
		if utilizador.username == username:
			return utilizador.userid

	return -1

#show the users in the room
def show_listed_users_impl(id_sala):
	key = ndb.Key(CheckRoom, int(id_sala))
	room = key.get()
	users = {}

	if room is None or len(room.userid) == 0: #there were no users in the room
		return {'state': 404, 'users': users} 
	else:
		for userident in room.userid:
			key_u=ndb.Key(User, int(userident))
			user_all=key_u.get()
			users[int(userident)]=user_all.username
		return {'state':200, 'users':users} # there were users in the room, return them

def rooms_ocupancy_impl():
	checkIns = CheckRoom.query().fetch()

	checkInByRoom = {}
	for checkIn in checkIns:
		if checkIn.roomid in checkInByRoom:
			checkInByRoom[checkIn.roomid] += 1
		else:
			checkInByRoom[checkIn.roomid] = 1

	return checkInByRoom

#check the user in the room if is a diferent one
def check_in_database_impl(data):
	roomid = data["roomid"]
	userid = data["uid"]

	key = ndb.Key(User, int(userid))
	user = key.get()
	if user != None: #check if the user is in the database
		if user.checked_in == -1: #the user was not in any room
			user.checked_in = int(roomid)
			user.put()
			key_cr = ndb.Key(CheckRoom, int(roomid))
			room = key_cr.get()
			if room != None: #there were users in the rooms add the new one
				buf = room.userid
				buf.append(int(userid))
				room.userid=buf
				room.put()

			else: #there was no one in the room
				checked_room = CheckRoom(roomid = int(roomid), userid = [int(userid)], key = ndb.Key(CheckRoom, int(roomid)))
				checked_room.put()

			return {'state': 201}

		elif user.checked_in == int(roomid): #user try to log in the same room
			return {'state': 400}
		else: #user was already logged in a room first logout then log in in the new one
			response=check_out_database_impl({'uid':userid})
			if (response['state']==200):
				response2=check_in_database_impl({'uid':userid, 'roomid':roomid})
				if (response2['state']==201):
					return {'state':200}
				else:
					return {'state':400}
			else:
				return {'state': 400}
			return {'state': 409}
	else:
		return {'state': 404}

#checkout the user from the room if it is in one
def check_out_database_impl(body):
	userid = body["uid"]

	key_u = ndb.Key(User, int(userid))
	user = key_u.get()
	if (user!=None): #check if user exists
		roomid = user.checked_in
		if roomid == -1: #the user was not in a room
			return {'state': 404}
		else: #the user was in a room, remove it
			user.checked_in = -1
			user.put()

			key_cr = ndb.Key(CheckRoom, int(roomid))
			room = key_cr.get()
			buf = room.userid
			buf.remove(int(userid))
			room.userid = buf
			room.put()
		return {'state': 200}

	else:
		return {'state': 404}

def is_room_provided_impl(roomId):
	try:
		roomIdParsed = str(roomId)
	except:
		return {'roomProvided': False}

	availableRooms = list_available_rooms()

	response = {'roomProvided': roomIdParsed in availableRooms}
	return response

def provideRoomImpl(roomId, roomName):
	sala = Room(roomName = roomName, roomId = roomId, key = ndb.Key(Room, int(roomId)))
	sala.saveToCloud()

# get userId from username
def convert_username(username):
	query = User.query().fetch()
	for utilizador in query:
		if username == utilizador.username:
			return username.userid

	return -1 #username didn't exist

def provide_room_impl(roomId, roomName):
	sala = Room(roomName = roomName, roomId = roomId, key = ndb.Key(Room, int(roomId)))
	sala.saveToCloud()

# show available rooms to check_in
def list_available_rooms():
	query = Room.query().fetch()
	available_rooms = {}
	for room in query:
		available_rooms[room.roomId]=room.roomName

	return available_rooms

#verify if the user is in a room
def is_user_checked_in(userId):
	key = ndb.Key(User, int(userId))
	user = key.get()

	if user.checked_in == -1: #the user was not in a room
		return 0
	else:
		return user.checked_in #return the id of the room where the user is