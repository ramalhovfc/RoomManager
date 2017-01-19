from bottle import Bottle, run, template, request, response, debug, get, post, static_file, redirect
from google.appengine.ext import ndb
import requests
import random
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

#ecra inicial e login do utilizador
@bottle.route('/')
def home():
	return templates.index

@bottle.route('/login', method="post")
def do_login():
	username = request.forms.get('username')
	#print ("O teu username e", username)
	userId = login_user(username)

	if userId < 0: #username already exists
		return template(templates.temp_login_user_doesnt_exists, username=username)

	elif userId == 0: #admin
		response.set_cookie("userId", str(userId))
		redirect("/admin")
	elif userId > 0: #regular user with valid username
		response.set_cookie("userId", str(userId))
		redirect("/user")

@bottle.route('/signin', method="post")
def do_signin():
	username = request.forms.get('username')
	#print ("O teu username e", username)
	userId = signin_user(username)

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
def adminArea():
	return template(templates.temp_adminArea)

@bottle.route('/admin/spaces', method="get")
def list_spaces():
	spaces = fenixFetcher.getSpaceById()
	return template(templates.temp_spaces, list = spaces)

@bottle.route('/admin/roomsOcupancy', method="get")
def roomsOcupancy():
	return template(templates.temp_roomsOcupancy, list = roomsOcupancyImpl(), get_url = bottle.get_url)

@bottle.route('/provideRoom/<roomId>/<roomName>', method="post")
def provideRoom(roomId, roomName):
	sala = Room(roomName = roomName, key = ndb.Key(Room, roomId))
	sala.saveToCloud()

@bottle.route('/admin/space/<id_space>')
def buildings(id_space):
	building = fenixFetcher.getSpaceById(id_space)
	if building["containedSpaces"] != []:
		return template(templates.temp_spaces, list = building["containedSpaces"], get_url = bottle.get_url)
	else:
		print ("cheguei a uma sala para reservar!")
		return template (templates.temp_provide, list = building, get_url = bottle.get_url)

@bottle.route('/isRoomProvided/<roomId>', method="get")
def provideRoom(roomId):
	return json.dumps(isRoomProvided(roomId))

@bottle.route('/user/<uid:int>/rooms')
def show_rooms(uid):
	rooms=list_available_rooms()
	id_rooms={}
	id_rooms["rooms"]=rooms
	id_rooms["id"]=uid
	print "rooms ---------------------------------------"
	print rooms
	return template(templates.temp, list= id_rooms, get_url = bottle.get_url)

@bottle.route('/api/checkin', method ="post")
def check_in_datase():
	#roomid = request.forms.get('roomid')
	#userid = request.forms.get('uid')

	data = json.load(request.body)
	roomid = data["roomid"]
	userid = data["uid"]

	print "Api funciona !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print userid, roomid
	#falta fazer query na base de dados para ver se utilziador ja fez check in

	key=ndb.Key(User, int(userid))
	user = key.get()

	if (user.checked_in == -1): #O utilizador nao estava logado em nenhuma sala
		user.checked_in = int(roomid)
		user.put()

		key_cr=ndb.Key(CheckRoom, int(roomid))
		exemplo=key_cr.get()
		if exemplo != None: #ja existiam utilizadores na sala, acrescentar o novo
			buf = exemplo.userid
			buf.append(int(userid))
			exemplo.userid=buf
			exemplo.put()

		else: #ainda nao existia ninguem na sala
			checked_room = CheckRoom(roomid = int(roomid), userid = [int(userid)])
			checked_room.key = ndb.Key(CheckRoom, int(roomid))
			checked_room.put()

		resposta = json.dumps({'state': 1})

	elif (user.checked_in == int(roomid)): #utilizador tenta fazer login na mesma sala
		resposta = json.dumps({'state': -1})
	else: #utilizador estava logado numa sala, primeiro fazer logout e depois voltar a fazer login
		resposta = json.dumps({'state': 0})

	return resposta

	#user_exemplo = User(username = username, userid = userid, checked_in = True)
	#user_exemplo.put()

@bottle.route('/api/checkout', method="post")
def check_out_database():
	#roomid = request.forms.get('roomid')
	#userid = request.forms.get('uid')
	#recebido = json.loads(request.body)

	userid2= json.load(request.body)
	userid = userid2["uid"]
	#print recebido
	print "fazer checkout ~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print userid
	#key_cr=ndb.Key(CheckRoom, int(roomid))
	#exemplo=key_cr.get()

#	if (exemplo!=None): #retirar utilizador da sala e alterar o seu estado para nao checked in
#		buf = exemplo.userid
#		buf.remove(userid)
#		exemplo.userid=buf
#		exemplo.put()
	key_u=ndb.Key(User, int(userid))
	exemplo2=key_u.get()
	roomid=exemplo2.checked_in
	if roomid == -1: #verificar se esta logado numa sala
		resposta = json.dumps({'state': 0})
	else:
		exemplo2.checked_in = -1
		exemplo2.put()
		resposta = json.dumps({'state': 1})

		key_cr=ndb.Key(CheckRoom, int(roomid))
		exemplo=key_cr.get()
		buf = exemplo.userid
		buf.remove(int(userid))
		exemplo.userid=buf
		exemplo.put()


	#resposta = {'state': 1}
	#resposta2=json.dumps(resposta)

	return resposta

def roomsOcupancyImpl():
	checkIns = CheckRoom.query().fetch()

	checkInByRoom = {}
	for checkIn in checkIns:
		if checkIn.roomId in checkInByRoom:
			checkInByRoom[checkIn.roomId] = checkInByRoom[checkIn.roomId] + 1
		else:
			checkInByRoom[checkIn.roomId] = 1

	return checkInByRoom

def isRoomProvided(roomId):
	try:
		roomIdParsed = str(roomId)
	except:
		return {'roomProvided': False}

	availableRooms = list_available_rooms()

	response = {'roomProvided': roomIdParsed in availableRooms}
	return response

def signin_user(username):
#verifica se o username ja existe
	max_userId=0
	if username != "admin":
		query=User.query().fetch()
		print query
		for utilizador in query:
			print utilizador
			if utilizador.userid>max_userId:
				max_userId=utilizador.userid
			if utilizador.username == username:
				return -1
		max_userId = max_userId + 1
		user_exemplo = User(username = username, userid = max_userId, checked_in = -1)
		user_exemplo.key = ndb.Key(User, max_userId)
		user_exemplo.put()
		return max_userId
	else:
		user_exemplo = User(username = username, userid = 0, checked_in = -1)
		user_exemplo.key = ndb.Key(User, max_userId)
		user_exemplo.put()
		return 0

def login_user(username):
	if username != "admin":
		query=User.query().fetch()
		for utilizador in query:
			if utilizador.username == username:
				return utilizador.userid

		return -1
	else:
		return 0

def convert_username(username):
	query=User.query().fetch()
	for utilizador in query:
		if username==utilizador.username:
			return username.userid

	return -1

#show available rooms to check_in
def list_available_rooms():
	query = Room.query().fetch()
	available_rooms = {}
	for room in query:
		available_rooms[room.roomId]=room.roomName

	return available_rooms


