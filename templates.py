#template for the main page of user
index = '''
    	<h2>Welcome to Room Management</h2>
    	<form action="/" method="post">
    		Username: <input name="username" type="text" /><br><br>
    		<button type="submit" formaction="/login">Login</button>
			<button type="submit" formaction="/signin">Signin</button>
    	</form>
'''

#template for the home page of the admin
adminArea = """
	<h2>Administrator Area</h2>
	<ol type="1">
		<li><a href="http://localhost:8080/admin/spaces">Search spaces</a></li>
		<li><a href="http://localhost:8080/admin/roomsOcupancy">List room ocupancy</a></li>
	</ol>
"""

#template to show the admin the available rooms and their occupancy
roomsOcupancy = """
	<h2>Room Ocupancy</h2>
	<table>
		<tr>
			<th>Room Id</th>
			<th>Ocupancy</th>
		</tr>
	% for key, value in list.items():
		<tr>
			<td>{{key}}</td>
			<td>{{value}}</td>
		</tr>
	% end
	</table>

	<br><br><a href="http://localhost:8080/admin">Admin menu</a>
"""

#template to show the spaces to the admin
spaces = """
<ol type="1">
	% if (list[0]["type"] == "FLOOR"):
		Floors 	<br><br>
	%end
	% for a in list:
		% if (a["name"] == ""):
			<li><a href="http://localhost:8080/admin/space/{{a["id"]}}"> {{a["id"]}} </a></li>
		% else:
			<li><a href="http://localhost:8080/admin/space/{{a["id"]}}"> {{a["name"]}} </a></li>
		%end
	% end
</ol>

<br><a href="http://localhost:8080/admin">Admin Menu</a>
"""

#template after the user correctly logged/signed in 
logged_in = """
		<br><a href="http://localhost:8080/user/rooms">List Available Rooms</a>

    	% if(list["checked_in"]==0):
        <br><br>You are not in a room <button id="Checkoutb" type="button" disabled onclick=checkoutuser({{list["uid"]}},1)> Check out </button>
    	% else:
        <br><br><span id="message">You are in room {{list["checked_in"]}} </span><button id="Checkoutb" type="button" onclick=checkoutuser({{list["uid"]}},1)> Check out </button>

		<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
"""

#template when the user chooses a username already taken
failed_login="""
	The username - {{username}} is already in use please choose another one
	<br><br><a href="http://localhost:8080/">Back to login</a>
"""

#template when the username of the login doesn't exist in the database
login_user_doesnt_exists="""
	The username - {{username}} does not exist, create it first
	<br><br><a href="http://localhost:8080/">Back to login</a>
"""

#template used to list all the available rooms that allow also to check in and see the users on each room
check_in = """<ol type="1">
	% for id_sala,name in list["rooms"].items():
		<li> {{id_sala}} - {{name}} <button id= "{{id_sala}}" type="button" onclick=checkinuser({{list["id"]}},{{id_sala}},1)> Check in </button>
		<button id ="{{id_sala}}+s" type="button" onclick=listusers({{id_sala}})> Show users </button></li>
	% end

    <br><a href="http://localhost:8080/user">Go Back</a>
</ol>

<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
"""
#template for the room to provide
provide = """
<ol>
	Type : {{list["type"]}} <br>
	Name : {{list["name"]}} <br>
	Campus : {{list["parentSpace"]["topLevelSpace"]["name"]}}<br> <br>

	<button id="provideButton" onclick="provideRoom({{list["id"]}}, \'{{list["name"]}}\')" disabled	>Checking if room is already provided...</button>

	<br><br><a href="http://localhost:8080/admin">Admin menu</a>

	<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
	<script type="text/javascript"> isRoomProvided({{list["id"]}}) </script>
</ol>"""
