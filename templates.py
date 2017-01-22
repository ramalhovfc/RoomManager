# template for the main page of user
index = '''
    	<h2>Welcome to Room Management</h2>
    	<form action="/" method="post">
    		Username: <input name="username" type="text" /><br><br>
    		<button type="submit" formaction="/login">Login</button>
			<button type="submit" formaction="/signin">Signin</button>
    	</form>
'''

# template for the home page of the admin
adminArea = """
	<h2>Administrator Area</h2>
	<ol type="1">
		<li><a href="http://{{serverHost}}{{serverPort}}/admin/spaces">Search spaces</a></li>
		<li><a href="http://{{serverHost}}{{serverPort}}/admin/spaces/ocupancy">List room ocupancy</a></li>
	</ol>

	<br><a href="http://{{serverHost}}{{serverPort}}/logout"> Logout </a>
"""

# template for trying to access admin page without logging as admin
notAdmin = """
	You are not an administrator!
	<br><br><a href="http://{{serverHost}}{{serverPort}}"> Login page </a>
"""

# template to show the admin the available rooms and their occupancy
roomsOcupancy = """
	<h2>Room Ocupancy</h2>
	<table>
		<tr>
			<th>Room Id</th>
			<th>Room Name</th>
			<th>Ocupancy</th>
		</tr>
	% for key, value in list.items():
		<tr>
			<td>{{key}}</td>
			<td>{{value["roomname"]}}</td>
			<td>{{value["ocupancy"]}}</td>
		</tr>
	% end
	</table>

	<br><br><a href="http://{{serverHost}}{{serverPort}}/admin">Admin menu</a>
"""

# template to show an error if an external system returns one
errorGettingSpaces = """
	Error getting spaces from external system
	<br><br><a href="http://{{serverHost}}{{serverPort}}/admin">Admin menu</a>
"""

# template to show the spaces to the admin
spaces = """
<ol type="1">
	% if (list[0]["type"] == "FLOOR"):
		Floors 	<br><br>
	%end
	% for a in list:
		% if (a["name"] == ""):
			<li><a href="http://{{serverHost}}{{serverPort}}/admin/space/{{a["id"]}}"> {{a["id"]}} </a></li>
		% else:
			<li><a href="http://{{serverHost}}{{serverPort}}/admin/space/{{a["id"]}}"> {{a["name"]}} </a></li>
		%end
	% end
</ol>

<br><a href="http://{{serverHost}}{{serverPort}}/admin">Admin Menu</a>
"""

# template after the user correctly logged/signed in
logged_in = """
		<br><a href="http://{{serverHost}}{{serverPort}}/user/rooms">List Available Rooms</a>

    	% if(list["checked_in"]==0):
        	<br><br>You are not in a room <button id="Checkoutb" type="button" disabled onclick=checkoutuser({{list["uid"]}},1)> Check out </button>
    	% else:
        	<br><br><span id="message">You are in room (id:{{list["checked_in"]}} name:{{list["name"]}})</span><button id="Checkoutb" type="button" onclick=checkoutuser({{list["uid"]}},1)> Check out </button>
		% end
		<br><br><a href="http://{{serverHost}}{{serverPort}}/logout"> Logout </a>

		<script type="text/javascript"> document.roomManager = { serverHost: '{{serverHost}}', serverPort: '{{serverPort}}' }; </script>
		<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
"""

# template when the user chooses a username already taken
failed_login="""
	The username - {{username}} is already in use please choose another one
	<br><br><a href="http://{{serverHost}}{{serverPort}}/">Back to login</a>
"""

# template for when the user is not logged in
notLoggedIn = """
	You are not logged in as a user
	<br><br><a href="http://{{serverHost}}{{serverPort}}/">Back to login</a>
"""

# template when the username of the login doesn't exist in the database
login_user_doesnt_exist="""
	The username {{username}} does not exist, create it first
	<br><br><a href="http://{{serverHost}}{{serverPort}}/">Back to login</a>
"""

# template used to list all the available rooms that allow also to check in and see the users on each room
check_in = """<ol type="1">
	% for id_sala,name in list["rooms"].items():
		<li> {{id_sala}} - {{name}} <button id= "{{id_sala}}" type="button" onclick=checkinuser({{list["id"]}},{{id_sala}},1)> Check in </button>
		<button id ="{{id_sala}}+s" type="button" onclick=listusers({{id_sala}})> Show users </button></li>
	% end

    <br><a href="http://{{serverHost}}{{serverPort}}/user">Go Back</a>
</ol>

<script type="text/javascript"> document.roomManager = { serverHost: '{{serverHost}}', serverPort: '{{serverPort}}' }; </script>
<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
"""
# template for the room to provide
provide = """
<ol>
	Type : {{list["type"]}} <br>
	Name : {{list["name"]}} <br>
	Campus : {{list["parentSpace"]["topLevelSpace"]["name"]}}<br> <br>

	<button id="provideButton" onclick="provideRoom({{list["id"]}}, \'{{list["name"]}}\')" disabled	>Checking if room is already provided...</button>
	<button id="deleteButton" onclick="deleteRoom({{list["id"]}})" disabled	>Delete</button>

	<br><br><a href="http://{{serverHost}}{{serverPort}}/admin">Admin menu</a>

	<script type="text/javascript"> document.roomManager = { serverHost: '{{serverHost}}', serverPort: '{{serverPort}}' }; </script>
	<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
	<script type="text/javascript"> isRoomProvided({{list["id"]}}) </script>
</ol>"""
