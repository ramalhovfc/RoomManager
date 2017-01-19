from bottle import Bottle, run, template, request, debug, get, post, static_file, redirect
from google.appengine.ext import ndb
import json
import requests
import random
import templates
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()

class User(ndb.Model):
	username = ndb.StringProperty()
	userid = ndb.IntegerProperty()
	checked_in = ndb.IntegerProperty()

class Room(ndb.Model):
	roomid = ndb.IntegerProperty()
	roomname = ndb.StringProperty()

class CheckRoom(ndb.Model):
	userid = ndb.IntegerProperty(repeated=True)
	roomid = ndb.IntegerProperty()

debug(True)

# Create the Bottle WSGI application.
bottle = Bottle()

@bottle.route('/js/:filename:')
def send_static(filename):
    return static_file(filename, root='./js/')

#ecra inicial e login do utilizador
@bottle.route('/')
def home():
    return templates.index

@bottle.route('/', method="post")
def do_login():
	username = request.forms.get('username')
	#print ("O teu username e", username)
	userid=login_user(username)
	if(userid<0): #username already exists
		return template(templates.temp_failed_login, username=username)
	elif (userid==0): #admin
		redirect("/0")
	elif (userid>0): #regular user with valid username
		redirect("/user/" +str(userid))
	#return template(templates.temp_utilizadores, list=utilizadores)
	
@bottle.route('/user/<uid:int>') #para identificar o admin
def user_actions(uid):
	return template(templates.logged_in, uid=uid)

@bottle.route('/0') #para identificar o admin
def list_spaces():
	#apagar esta linha
	criar_sala()
	inserir_user_sala()

	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces')
	spaces = json.loads(r.text)
	return template (templates.temp_spaces ,list = spaces)

@bottle.route('/0/space/<id_space:int>')
def buildings(id_space):
	complete_path = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+str(id_space)
	r = requests.get(complete_path)
	building = json.loads(r.text)
	if (building["containedSpaces"] != []):
		return template (templates.temp_spaces, list = building["containedSpaces"])
	else:
		print ("cheguei a uma sala para reservar!")
		return template (templates.temp_provide, list = building) 	

@bottle.route('/user/<uid:int>/rooms')
def show_rooms(uid):
	rooms=list_available_rooms()
	id_rooms={}
	id_rooms["rooms"]=rooms
	id_rooms["id"]=uid
	print "rooms ---------------------------------------"
	print rooms
	return template(templates.temp, list= id_rooms)

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


#	else: # a fazer depois quando a sala nao esta na base de dados
#		print("dsfasdfsdfas")

"""@bottle.route('/api/listusers/<id_sala:int>')
def show_listed_users_api(id_sala):
	redirect("/listusers/"+int(id_sala))
"""

@bottle.route('/api/listusers/<id_sala:int>')
def show_listed_users(id_sala):

	key=ndb.Key(CheckRoom, int(id_sala))
	room=key.get()

	users = {}

	#print room.userid

	if (room is None):
		resposta = {'state':0, 'users':users} #Nao esta ninguem logado na sala 
	else:
		for userident in room.userid:
			#print int(userident)
			key_u=ndb.Key(User, int(userident))
			user_all=key_u.get()
			users[int(userident)]=user_all.username
		resposta = {'state':1, 'users':users} #existem utilizadores logados na sala	

	return  json.dumps(resposta) #nao esta a mudar de pagina com o template, javascript ver

def login_user(username):
#verifica se o username ja existe 
	max_userid=0
	if (username!="admin"):
		query=User.query().fetch()
		print query
		for utilizador in query:
			print utilizador
			if utilizador.userid>max_userid:
				max_userid=utilizador.userid
			if utilizador.username == username:
				return -1
		max_userid=max_userid+1
		user_exemplo = User(username = username, userid = max_userid, checked_in = -1)
		user_exemplo.key = ndb.Key(User, max_userid)
		user_exemplo.put()
		return max_userid
	else:
		user_exemplo = User(username = username, userid = 0,  checked_in = -1)
		user_exemplo.key = ndb.Key(User, max_userid)
		user_exemplo.put()
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
		available_rooms[room.roomid]=room.roomname
		print room.roomid," ",room.roomname	

	return available_rooms

#apagar, funcao de teste
def criar_sala():
	sala_exemplo = Room(roomid = 1234, roomname = "sala 1")
	sala_exemplo.key = ndb.Key(Room, 1234)
	sala_exemplo.put()

	sala_exemplo2 = Room(roomid = 567, roomname = "sala 2")
	sala_exemplo2.key = ndb.Key(Room, 567)
	sala_exemplo2.put()

	sala_exemplo3 = Room(roomid = 89, roomname = "sala 3")
	sala_exemplo3.key = ndb.Key(Room, 89)
	sala_exemplo3.put()

#funcao de teste apagar
def inserir_user_sala():
	room = CheckRoom(roomid = 89, userid =[1,2,3])
	room.put()

	"""room2 = CheckRoom(roomid = 89, userid = 2)
	room2.put()

	room3 = CheckRoom(roomid = 89, userid = 3)
	room3.put()"""

	room4 = CheckRoom(roomid = 1234, userid = [1])
	room4.put()

	room5 = CheckRoom(roomid = 567, userid = [1])
	room5.put()

	#room6 = CheckRoom(roomid = 1234, userid = 1)
	#room6.put()


"""if __name__=="__main__":
	debug()
	run(app, host='localhost', port=8080, reloader=True) #Run starts to build-in a development server
"""
