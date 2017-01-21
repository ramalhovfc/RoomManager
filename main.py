from bottle import Bottle, template, request, response, debug, static_file, redirect
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

# TODO feed js url through python

# servir javascript independentemente do url
@bottle.route('/static/<filename>', name = 'static')
def server_static(filename):
	return static_file(filename, root = 'static')

# ecra inicial e login do utilizador
@bottle.route('/')
def home():
	response.set_cookie('userId', '', expires = 0)
	return templates.index

@bottle.route('/logout')
def do_logout():
	response.set_cookie('userId', '', expires = 0)
	redirect("/")

@bottle.route('/login', method = "post")
def do_login():
	username = request.forms.get('username')
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

	if userId is None or userId == "" or userId == "0":
		return template(templates.notLoggedIn, get_url = bottle.get_url)

	user_state = { "uid": userId, "checked_in": mainImpl.is_user_checked_in(userId) }

	return template(templates.logged_in, list = user_state, get_url = bottle.get_url)

@bottle.route('/admin')
def adminArea():
	userId = request.get_cookie("userId")
	if userId != "0":
		return template(templates.notAdmin, get_url = bottle.get_url)

	return template(templates.adminArea, get_url = bottle.get_url)

@bottle.route('/admin/spaces', method = "get")
def list_spaces():
	try:
		building = fenixFetcher.getSpaceById()
	except:
		return template(templates.errorGettingSpaces)
	return template(templates.spaces, list = building, get_url = bottle.get_url)

@bottle.route('/admin/spaces/ocupancy')
def roomsOcupancy():
	return template(templates.roomsOcupancy, list = mainImpl.rooms_ocupancy_impl(), get_url = bottle.get_url)

@bottle.route('/api/spaces/provide/<roomId>/<roomName>', method= "post")
def provideRoom(roomId, roomName):
	mainImpl.provide_room_impl(roomId, roomName)

@bottle.route('/admin/space/<id_space>')
def buildings(id_space):
	try:
		building = fenixFetcher.getSpaceById(id_space)
	except:
		return template(templates.errorGettingSpaces)

	if building["containedSpaces"] != []:
		return template(templates.spaces, list = building["containedSpaces"], get_url = bottle.get_url)
	else:
		return template(templates.provide, list = building, get_url = bottle.get_url)

@bottle.route('/admin/spaces/provided/<roomId>')
def is_room_provided(roomId):
	return json.dumps({"roomProvided": mainImpl.is_room_provided_impl(roomId)})

@bottle.route('/user/rooms')
def show_rooms():
	uid = request.get_cookie("userId")
	rooms = mainImpl.list_available_rooms()
	id_rooms = { "rooms": rooms, "id": uid }
	return template(templates.check_in, list = id_rooms, get_url = bottle.get_url)

@bottle.route('/api/checkin', method = "post")
def check_in_database():
	return json.dumps(mainImpl.check_in_database_impl(json.load(request.body)))

@bottle.route('/api/checkout', method = "post")
def check_out_database():
	return json.dumps(mainImpl.check_out_database_impl(json.load(request.body)))

@bottle.route('/api/listusers/<id_sala:int>')
def show_listed_users(id_sala):
	return json.dumps(mainImpl.show_listed_users_impl(id_sala))

