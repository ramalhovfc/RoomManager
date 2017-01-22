from bottle import Bottle, template, request, response, debug, static_file, redirect, HTTPResponse
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

# serve static files, url independant
@bottle.route('/static/<filename>', name = 'static')
def server_static(filename):
	return static_file(filename, root = 'static')

# initial login/signin screen
@bottle.route('/', method = "get")
def home():
	response.set_cookie('userId', '', expires = 0)
	return templates.index

# logout endpoint. clear cookie and redirect to initial screen
@bottle.route('/logout', method = "get")
def do_logout():
	response.set_cookie('userId', '', expires = 0)
	redirect("/")

# login endpoint
@bottle.route('/login', method = "post")
def do_login():
	username = request.forms.get('username')
	userId = mainImpl.login_user_impl(username)

	if userId < 0: # username does not exist
		return template(templates.login_user_doesnt_exist, username = username, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')

	elif userId == 0: # admin
		response.set_cookie("userId", str(userId))
		redirect("/admin")

	elif userId > 0: # regular user with valid username
		response.set_cookie("userId", str(userId))
		redirect("/user")

# api login endpoint
@bottle.route('/api/login', method = "post")
def do_api_login():
	try:
		username = str(request.POST.get("username"))
	except:
		return json.dumps({"state": 400, "msg": "No username provided"})

	if username == "":
		return json.dumps({"state": 400, "msg": "Empty username"})

	userId = mainImpl.login_user_impl(username)

	if userId < 0: # username does not exist
		return json.dumps({"state": 404, "msg": "User does not exist"})

	response.set_cookie("userId", str(userId))
	return json.dumps({"state": 200, "msg": userId})

# signin endpoint
@bottle.route('/signin', method = "post")
def do_signin():
	username = request.forms.get('username')
	userId = mainImpl.signin_user_impl(username)

	if userId < 0: # username already exists
		return template(templates.failed_login, username = username, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')

	elif userId == 0: # admin
		response.set_cookie("userId", str(userId))
		redirect("/admin")
	elif userId > 0: # regular user with valid username
		response.set_cookie("userId", str(userId))
		redirect("/user")

# api signin endpoint
@bottle.route('/api/signin', method = "post")
def do_api_signin():
	try:
		username = str(request.POST.get("username"))
	except:
		return json.dumps({"state": 400, "msg": "No username provided"})

	if username == "":
		return json.dumps({"state": 400, "msg": "Empty username"})

	userId = mainImpl.signin_user_impl(username)

	if userId < 0: # username already exists
		return json.dumps({"state": 409, "msg": "Username already exists"})

	response.set_cookie("userId", str(userId))
	return json.dumps({"state": 200, "msg": username})

# main user page
@bottle.route('/user', method = "get")
def user_actions():
	userId = request.get_cookie("userId")

	if userId is None or userId == "" or userId == "0":
		return template(templates.notLoggedIn, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')

	log_in = mainImpl.is_user_checked_in(userId)
	if log_in['state'] == 0:
		user_state = {"uid": userId, "checked_in": 0, "name": "no room"}
	else:
		user_state = {"uid": userId, "checked_in": log_in['userid'], "name": log_in['roomname']}

	return template(templates.logged_in, list = user_state, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')

# main admin page
@bottle.route('/admin', method = "get")
def adminArea():
	userId = request.get_cookie("userId")
	if userId != "0":
		return template(templates.notAdmin, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')

	return template(templates.adminArea, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')

# browser spaces screen
@bottle.route('/admin/spaces', method = "get")
def list_spaces():
	try:
		building = fenixFetcher.getSpaceById()
	except:
		return template(templates.errorGettingSpaces, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')
	return template(templates.spaces, list = building, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')

# list room ocupancy page
@bottle.route('/api/admin/spaces/ocupancy', method = "get")
@bottle.route('/admin/spaces/ocupancy', method = "get")
def roomsOcupancy():
	if request['bottle.route'].rule == '/admin/spaces/ocupancy': # accessed from the browser, return the template
		return template(templates.roomsOcupancy, list = mainImpl.rooms_ocupancy_impl(), get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')
	elif request['bottle.route'].rule == '/api/admin/spaces/ocupancy':
		return json.dumps(mainImpl.rooms_ocupancy_impl())

# endpoint to provide/add a room
@bottle.route('/api/spaces/provide/<roomId>/<roomName>', method = "post")
def provideRoom(roomId, roomName):
	mainImpl.provide_room_impl(roomId, roomName)

# endpoint to delete a room
@bottle.route('/api/spaces/provide/<roomId>', method = "delete")
def provideRoom(roomId):
	mainImpl.delete_room_impl(roomId)

# admin browse spaces page
@bottle.route('/admin/space/<id_space>', method = "get")
def buildings(id_space):
	try:
		building = fenixFetcher.getSpaceById(id_space)
	except:
		return template(templates.errorGettingSpaces, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')

	if building["containedSpaces"] != []:
		return template(templates.spaces, list = building["containedSpaces"], get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')
	else:
		return template(templates.provide, list = building, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')

# endpoint to tell if a room is provided or not
@bottle.route('/admin/spaces/provided/<roomId>', method = "get")
def is_room_provided(roomId):
	return json.dumps({"roomProvided": mainImpl.is_room_provided_impl(roomId)})

# page to see where the user can checkin in rooms and see where he is checked in
@bottle.route('/api/user/rooms', method = "get")
@bottle.route('/user/rooms', method = "get")
def show_rooms():
	uid = request.get_cookie("userId")
	rooms = mainImpl.list_available_rooms()
	id_rooms = { "rooms": rooms, "id": uid }

	if request['bottle.route'].rule == '/user/rooms': # accessed from the browser, return the template
		return template(templates.check_in, list = id_rooms, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = ':8080' if request.get_header('host') == 'localhost' else '')
	elif request['bottle.route'].rule == '/api/user/rooms': # just the rest answer
		return json.dumps(id_rooms)

# endpoint to provide checkin functionality
@bottle.route('/api/checkin', method = "put")
def check_in_database():
	return json.dumps(mainImpl.check_in_database_impl(json.load(request.body)))

# endpoint to provide checkout functionality
@bottle.route('/api/checkout', method = "put")
def check_out_database():
	return json.dumps(mainImpl.check_out_database_impl(json.load(request.body)))

# endpoint to list users that checked-in in a room
@bottle.route('/api/listusers/<id_sala:int>', method = "get")
def show_listed_users(id_sala):
	return json.dumps(mainImpl.show_listed_users_impl(id_sala))
