from bottle import Bottle, template, request, response, debug, get, post, static_file, redirect
import templates
import requests_toolbelt.adapters.appengine
import json
from google.appengine.ext import ndb

from CheckRoom import CheckRoom
from Room import Room
from User import User
from SpaceFetcher import SpaceFetcher

requests_toolbelt.adapters.appengine.monkeypatch()

fenixFetcher = SpaceFetcher("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")

debug(True)

# Create the Bottle WSGI application.
bottle = Bottle()

@bottle.route('/static/<filename>', name='static')
def server_static(filename):
	return static_file(filename, root='static')

@bottle.route('/')
def home():
	return templates.index

@bottle.route('/', method="post")
def do_login():
	username = request.forms.get('username')
	#print ("O teu username e", username)
	userId = login_user(username)

	if userId < 0: #username already exists
		return template(templates.temp_failed_login, username=username)

	elif userId == 0: #admin
		response.set_cookie("userId", str(userId))
		redirect("/admin")
	elif userId > 0: #regular user with valid username
		response.set_cookie("userId", str(userId))
		redirect("/user")

@bottle.route('/user')
def user_actions():
	userId = request.get_cookie("userId")
	return template(templates.logged_in, uid = userId, get_url = bottle.get_url)

@bottle.route('/admin')
def list_spaces():
	spaces = fenixFetcher.getSpaceById()
	return template(templates.temp_spaces, list = spaces)

@bottle.route('/provideRoom/<roomId>/<roomName>', method="post")
def provideRoom(roomId, roomName):
	criar_sala(int(roomId), roomName)

@bottle.route('/isRoomProvided/<roomId>', method="get")
def provideRoom(roomId):
	return str(isRoomProvided(roomId))

@bottle.route('/testing', method="post")
def testing():
	print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
	return str(json.load(request.body))

@bottle.route('/0/space/<id_space>')
def buildings(id_space):
	building = fenixFetcher.getSpaceById(id_space)
	if (building["containedSpaces"] != []):
		return template(templates.temp_spaces, list = building["containedSpaces"], get_url = bottle.get_url)
	else:
		print ("cheguei a uma sala para reservar!")
		return template (templates.temp_provide, list = building, get_url = bottle.get_url)

@bottle.route('/user/<uid:int>/rooms')
def show_rooms(uid):
	rooms=list_available_rooms()
	id_rooms={}
	id_rooms["rooms"]=rooms
	id_rooms["id"]=uid
	print "rooms ---------------------------------------"
	print rooms
	return template(templates.temp, list= id_rooms, get_url = bottle.get_url)

@bottle.route('/api/checkin', method ="post") #pode ser feito assim ou passando as coisas pelo url
def check_in_datase():
	roomId = request.forms.get('roomId')
	userId = request.forms.get('uid')

	print "Api funciona !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print userId, roomId
	#falta fazer query na base de dados para ver se utilziador ja fez check in
	key_cr=ndb.Key(CheckRoom, int(roomId))
	exemplo=key_cr.get()
	print "===================================================="
	if exemplo != None:
		buf = exemplo.userId
		buf.append(int(userId))
		exemplo.userId=buf
		exemplo.put()

	else:
		checked_room = CheckRoom(roomId = int(roomId), userId = [int(userId)])
		checked_room.key = ndb.Key(CheckRoom, int(roomId))
		checked_room.put()


	key=ndb.Key(User, int(userId))
	user = key.get()
	user.checked_in = True
	user.put()

	#user_exemplo = User(username = username, userId = userId, checked_in = True)
	#user_exemplo.put()

@bottle.route('api/checkout', method="post")
def check_out_database():
	roomId = request.forms.get('roomId')
	userId = request.forms.get('uid')

	print "fazer checkout"

	key_cr=ndb.Key(CheckRoom, int(roomId))
	exemplo=key_cr.get()

	if (exemplo!=None):
		print("none")
	else: # a fazer depois quando o utilizador nao esta na sala
		print("dsfasdfsdfas")

def isRoomProvided(roomId):
	try:
		roomIdParsed = int(roomId)
	except:
		return str(False)

	availableRooms = list_available_rooms()
	return str(roomId in availableRooms)

def login_user(username):
#verifica se o username ja existe
	max_userId=0
	if (username!="admin"):
		query=User.query().fetch()
		print query
		for utilizador in query:
			print utilizador
			if utilizador.userId>max_userId:
				max_userId=utilizador.userId
			if utilizador.username == username:
				return -1
		max_userId=max_userId+1
		user_exemplo = User(username = username, userId = max_userId, checked_in = False)
		user_exemplo.key = ndb.Key(User, max_userId)
		user_exemplo.put()
		return max_userId
	else:
		user_exemplo = User(username = username, userId = 0,  checked_in = False)
		user_exemplo.key = ndb.Key(User, max_userId)
		user_exemplo.put()
		return 0

def convert_username(username):
	query=User.query().fetch()
	for utilizador in query:
		if username==utilizador.username:
			return username.userId

	return -1

#show available rooms to check_in
def list_available_rooms():
	query = Room.query().fetch()
	available_rooms = {}
	for room in query:
		available_rooms[room.key]=room.roomName
		print room.key," ",room.roomName

	return available_rooms

#apagar, funcao de teste
def criar_sala(roomId, roomName):
	sala = Room(roomId = roomId, roomName = roomName)
	sala.saveToCloud()

#funcao de teste apagar
def inserir_user_sala():
	room = CheckRoom(roomId = 89, userId =[1,2,3])
	room.put()

	"""room2 = CheckRoom(roomId = 89, userId = 2)
	room2.put()

	room3 = CheckRoom(roomId = 89, userId = 3)
	room3.put()"""

	room4 = CheckRoom(roomId = 1234, userId = [1])
	room4.put()

	room5 = CheckRoom(roomId = 567, userId = [1])
	room5.put()

	#room6 = CheckRoom(roomId = 1234, userId = 1)
	#room6.put()


"""if __name__=="__main__":
	debug()
	run(app, host='localhost', port=8080, reloader=True) #Run starts to build-in a development server
"""
