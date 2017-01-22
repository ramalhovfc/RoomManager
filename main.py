from bottle import Bottle, template, request, response, debug, static_file, redirect, HTTPResponse
import requests_toolbelt.adapters.appengine
import templates
import json
import logging

requests_toolbelt.adapters.appengine.monkeypatch()

import mainImpl

from SpaceFetcher import SpaceFetcher
fenixFetcher = SpaceFetcher("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")

debug(True)

# Create the Bottle WSGI application.
bottle = Bottle()

# servir javascript independentemente do url
@bottle.route('/static/<filename>', name = 'static')
def server_static(filename):
	return static_file(filename, root = 'static')

# ecra inicial e login do utilizador
@bottle.route('/', method = "get")
def home():
	response.set_cookie('userId', '', expires = 0)
	return templates.index

@bottle.route('/logout', method = "get")
def do_logout():
	response.set_cookie('userId', '', expires = 0)
	redirect("/")

@bottle.route('/login', method = "post")
def do_login():
	username = request.forms.get('username')
	userId = mainImpl.login_user_impl(username)

	if userId < 0: # username does not exist
		return template(templates.login_user_doesnt_exist, username = username, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))

	elif userId == 0: # admin
		response.set_cookie("userId", str(userId))
		redirect("/admin")

	elif userId > 0: # regular user with valid username
		response.set_cookie("userId", str(userId))
		redirect("/user")

@bottle.route('/api/login', method = "post")
def do_api_login():
	try:
		logging.error("11111111111111111111111111111")
		logging.error(request)
		body = json.load(request.body)
	except:
		logging.error("3333333333333333")
		return HTTPResponse(status = 400)

	logging.error("2222222222222222222222")
	if body["username"] is None or body["username"] == "":
		return HTTPResponse(status = 400)

	username = body["username"]
	userId = mainImpl.login_user_impl(username)

	if userId < 0: # username does not exist
		return HTTPResponse(status = 404, body = "User does not exist")

	response.set_cookie("userId", str(userId))
	HTTPResponse(status = 200, body = userId)

@bottle.route('/signin', method = "post")
def do_signin():
	username = request.forms.get('username')
	userId = mainImpl.signin_user_impl(username)

	if userId < 0: # username already exists
		return template(templates.failed_login, username = username, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))

	elif userId == 0: # admin
		response.set_cookie("userId", str(userId))
		redirect("/admin")
	elif userId > 0: # regular user with valid username
		response.set_cookie("userId", str(userId))
		redirect("/user")

@bottle.route('/api/signin', method = "post")
def do_api_signin():
	try:
		body = json.load(request.body)
	except:
		return HTTPResponse(status = 400)

	if body["username"] is None or body["username"] == "":
		return HTTPResponse(status = 400)

	username = body["username"]
	userId = mainImpl.signin_user_impl(username)

	if userId < 0: # username already exists
		return HTTPResponse(status = 409, body = "Username already exists")

	response.set_cookie("userId", str(userId))

@bottle.route('/user', method ="get")
def user_actions():
	userId = request.get_cookie("userId")

	if userId is None or userId == "" or userId == "0":
		return template(templates.notLoggedIn, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))

	user_state = { "uid": userId, "checked_in": mainImpl.is_user_checked_in(userId) }

	return template(templates.logged_in, list = user_state, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))

@bottle.route('/admin', method = "get")
def adminArea():
	userId = request.get_cookie("userId")
	if userId != "0":
		return template(templates.notAdmin, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))

	return template(templates.adminArea, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))

@bottle.route('/admin/spaces', method = "get")
def list_spaces():
	try:
		building = fenixFetcher.getSpaceById()
	except:
		return template(templates.errorGettingSpaces, serverHost = request.get_header('host'), serverPort = request.get_header('port'))
	return template(templates.spaces, list = building, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))

@bottle.route('/api/admin/spaces/ocupancy', method = "get")
@bottle.route('/admin/spaces/ocupancy', method = "get")
def roomsOcupancy():
	if request['bottle.route'].rule == '/admin/spaces/ocupancy': # accessed from the browser, return the template
		return template(templates.roomsOcupancy, list = mainImpl.rooms_ocupancy_impl(), get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))
	elif request['bottle.route'].rule == '/api/admin/spaces/ocupancy':
		return json.dumps(mainImpl.rooms_ocupancy_impl())

@bottle.route('/api/spaces/provide/<roomId>/<roomName>', method = "post")
def provideRoom(roomId, roomName):
	mainImpl.provide_room_impl(roomId, roomName)

@bottle.route('/admin/space/<id_space>', method = "get")
def buildings(id_space):
	try:
		building = fenixFetcher.getSpaceById(id_space)
	except:
		return template(templates.errorGettingSpaces, serverHost = request.get_header('host'), serverPort = request.get_header('port'))

	if building["containedSpaces"] != []:
		return template(templates.spaces, list = building["containedSpaces"], get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))
	else:
		return template(templates.provide, list = building, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))

@bottle.route('/admin/spaces/provided/<roomId>', method = "get")
def is_room_provided(roomId):
	return json.dumps({"roomProvided": mainImpl.is_room_provided_impl(roomId)})

@bottle.route('/api/user/rooms', method = "get")
@bottle.route('/user/rooms', method = "get")
def show_rooms():
	uid = request.get_cookie("userId")
	rooms = mainImpl.list_available_rooms()
	id_rooms = { "rooms": rooms, "id": uid }

	if request['bottle.route'].rule == '/user/rooms': # accessed from the browser, return the template
		return template(templates.check_in, list = id_rooms, get_url = bottle.get_url, serverHost = request.get_header('host'), serverPort = request.get_header('port'))
	elif request['bottle.route'].rule == '/api/user/rooms': # just the rest answer
		return json.dumps(id_rooms)

@bottle.route('/api/checkin', method = "put")
def check_in_database():
	return json.dumps(mainImpl.check_in_database_impl(json.load(request.body)))

@bottle.route('/api/checkout', method = "put")
def check_out_database():
	return json.dumps(mainImpl.check_out_database_impl(json.load(request.body)))

@bottle.route('/api/listusers/<id_sala:int>', method = "get")
def show_listed_users(id_sala):
	return json.dumps(mainImpl.show_listed_users_impl(id_sala))
