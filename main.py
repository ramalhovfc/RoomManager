from bottle import Bottle, template, request, response, debug, static_file, redirect
import requests_toolbelt.adapters.appengine
import templates
import json

requests_toolbelt.adapters.appengine.monkeypatch()

import mainImpl

from SpaceFetcher import SpaceFetcher
fenixFetcher = SpaceFetcher("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")

debug(True)

# Create the Bottle WSGI application.
bottle = Bottle()

# TODO add checkroom when adding room
# TODO feed js url through python
# TODO logout button

# servir javascript independentemente do url
@bottle.route('/static/<filename>', name = 'static')
def server_static(filename):
	return static_file(filename, root = 'static')

# ecra inicial e login do utilizador
@bottle.route('/')
def home():
	return templates.index

@bottle.route('/login', method = "post")
def do_login():
	username = request.forms.get('username')
	#print ("O teu username e", username)
	userId = mainImpl.login_user_impl(username)

	if userId < 0: # username already exists
		return template(templates.login_user_doesnt_exists, username = username, get_url = bottle.get_url)

	elif userId == 0: # admin
		response.set_cookie("userId", str(userId))
		redirect("/admin")
	elif userId > 0: # regular user with valid username
		response.set_cookie("userId", str(userId))
		redirect("/user")

@bottle.route('/signin', method = "post")
def do_signin():
	username = request.forms.get('username')
	userId = mainImpl.signin_user_impl(username)

	if userId < 0: # username already exists
		return template(templates.failed_login, username = username, get_url = bottle.get_url)

	elif userId == 0: # admin
		response.set_cookie("userId", str(userId))
		redirect("/admin")
	elif userId > 0: # regular user with valid username
		response.set_cookie("userId", str(userId))
		redirect("/user")

@bottle.route('/user')
def user_actions():
	userId = request.get_cookie("userId")
	user_state = { "uid": userId, "checked_in": mainImpl.is_user_checked_in(userId) }

	return template(templates.logged_in, list = user_state, get_url = bottle.get_url)

@bottle.route('/admin')
def adminArea():
	return template(templates.adminArea, get_url = bottle.get_url)

@bottle.route('/admin/spaces', method = "get")
def list_spaces():
	return template(templates.spaces, list = fenixFetcher.getSpaceById(), get_url = bottle.get_url)

@bottle.route('/admin/roomsOcupancy', method = "get")
def roomsOcupancy():
	return template(templates.roomsOcupancy, list = mainImpl.rooms_ocupancy_impl(), get_url = bottle.get_url)

@bottle.route('/api/provideRoom/<roomId>/<roomName>', method= "post")
def provideRoom(roomId, roomName):
	mainImpl.provide_room_impl(roomId, roomName)

@bottle.route('/admin/space/<id_space>')
def buildings(id_space):
	building = fenixFetcher.getSpaceById(id_space)
	if building["containedSpaces"] != []:
		return template(templates.spaces, list = building["containedSpaces"], get_url = bottle.get_url)
	else:
		return template(templates.provide, list = building, get_url = bottle.get_url)

@bottle.route('/isRoomProvided/<roomId>', method = "get")
def is_room_provided(roomId):
	return json.dumps(mainImpl.is_room_provided_impl(roomId))

@bottle.route('/api/user/rooms', method = 'get')
@bottle.route('/user/rooms', method ="get")
def show_rooms():
	uid = request.get_cookie("userId")
	rooms = mainImpl.list_available_rooms()
	id_rooms = { "rooms": rooms, "id": uid }

	if (request['bottle.route'].rule == '/user/rooms'): #accessed from the browser, return the template
		return template(templates.check_in, list = id_rooms, get_url = bottle.get_url) 
	elif (request['bottle.route'].rule == '/api/user/rooms'): #just the rest answer
		return id_rooms


@bottle.route('/api/checkin', method = "put")
def check_in_database():
	return json.dumps(mainImpl.check_in_database_impl(json.load(request.body)))

@bottle.route('/api/checkout', method = "put")
def check_out_database():
	return json.dumps(mainImpl.check_out_database_impl(json.load(request.body)))

@bottle.route('/api/listusers/<id_sala:int>', method = "get")
def show_listed_users(id_sala):
	return json.dumps(mainImpl.show_listed_users_impl(id_sala))

