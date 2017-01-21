from google.appengine.ext import ndb

from User import User
from CheckRoom import CheckRoom

def signin_user_impl(username):
	# verifica se o username ja existe
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
		user_exemplo.saveToCloud()
		return max_userId
	else:
		user_exemplo = User(username = username, userid = 0, checked_in = -1, key = ndb.Key(User, 0))
		user_exemplo.saveToCloud()
		return 0

def login_user_impl(username):
	query = User.query().fetch()
	for utilizador in query:
		if utilizador.username == username:
			return utilizador.userid

	return -1

def show_listed_users_impl(id_sala):
	key = ndb.Key(CheckRoom, int(id_sala))
	room = key.get()
	users = {}

	if room is None or len(room.userid) == 0:
		return {'state': 0, 'users': users} # Nao esta ninguem logado na sala
	else:
		for userident in room.userid:
			#print int(userident)
			key_u = ndb.Key(User, int(userident))
			user_all = key_u.get()
			users[int(userident)] = user_all.username
		return {'state': 1, 'users': users} # existem utilizadores logados na sala

def rooms_ocupancy_impl():
	checkIns = CheckRoom.query().fetch()

	checkInByRoom = {}
	for checkIn in checkIns:
		checkInByRoom[checkIn.roomid] = {"ocupancy": len(checkIn.userid), "roomname": checkIn.roomname}

	return checkInByRoom

def check_in_database_impl(data):
	roomid = data["roomid"]
	userid = data["uid"]

	key = ndb.Key(User, int(userid))
	user = key.get()

	if user.checked_in == -1: # O utilizador nao estava logado em nenhuma sala
		user.checked_in = int(roomid)
		user.saveToCloud()

		key_cr = ndb.Key(CheckRoom, int(roomid))
		exemplo = key_cr.get()
		buf = exemplo.userid
		buf.append(int(userid))
		exemplo.userid = buf
		exemplo.saveToCloud()

		return {'state': 1}

	elif user.checked_in == int(roomid): # utilizador tenta fazer login na mesma sala
		return {'state': -1}
	else: # utilizador estava logado numa sala, primeiro fazer logout e depois voltar a fazer login
		return {'state': 0}

def check_out_database_impl(body):
	userid = body["uid"]

	key_u = ndb.Key(User, int(userid))
	exemplo2 = key_u.get()
	roomid = exemplo2.checked_in
	if roomid == -1: # verificar se esta logado numa sala
		return {'state': 0}
	else:
		exemplo2.checked_in = -1
		exemplo2.saveToCloud()

		key_cr = ndb.Key(CheckRoom, int(roomid))
		exemplo = key_cr.get()
		buf = exemplo.userid
		buf.remove(int(userid))
		exemplo.userid = buf
		exemplo.saveToCloud()

	return {'state': 1}

def is_room_provided_impl(roomId):
	try:
		roomIdParsed = int(roomId)
	except:
		return False

	key = ndb.Key(CheckRoom, roomIdParsed)
	room = key.get()
	if room is None:
		return False
	else:
		return True

# get userId from username
def convert_username(username):
	query = User.query().fetch()
	for utilizador in query:
		if username == utilizador.username:
			return username.userid

	return -1

def provide_room_impl(roomid, roomname):
	checked_room = CheckRoom(roomid = int(roomid), userid = [], roomname = roomname, key = ndb.Key(CheckRoom, int(roomid)))
	checked_room.saveToCloud()

# show available rooms to check_in
def list_available_rooms():
	query = CheckRoom.query().fetch()
	available_rooms = {}
	for room in query:
		available_rooms[room.roomid] = room.roomname

	return available_rooms

def is_user_checked_in(userId):
	# verifica se o utilizador esta nalguma sala
	key = ndb.Key(User, int(userId))
	user = key.get()

	if user.checked_in == -1: # O utilizador nao estava logado em nenhuma sala
		return 0
	else:
		return 1
