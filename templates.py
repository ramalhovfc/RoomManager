index = '''
    	<h2>Welcome to Room Management</h2>
    	<form action="/" method="post">
    		Username: <input name="username" type="text" /><br><br>
    		<button type="submit" formaction="/login">Login</button>
			<button type="submit" formaction="/signin">Signin</button>
    	</form>
'''

adminArea = """
	<h2>Administrator Area</h2>
	<ol type="1">
		<li><a href="http://localhost:8080/admin/spaces">Search spaces</a></li>
		<li><a href="http://localhost:8080/admin/spaces/ocupancy">List room ocupancy</a></li>
	</ol>

	<br><a href="http://localhost:8080/logout"> Logout </a>
"""

notAdmin = """
	You are not an administrator!

	<br><br><a href="http://localhost:8080"> Login page </a>
"""

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

	<br><br><a href="http://localhost:8080/admin">Admin menu</a>
"""

errorGettingSpaces = """
	Error getting spaces from external system

	<br><br><a href="http://localhost:8080/admin">Admin menu</a>
"""

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

logged_in = """
		<br><a href="http://localhost:8080/user/rooms">List Available Rooms</a>

    	% if(list["checked_in"]==0):
        <br><br>You are not in a room <button id="Checkoutb" type="button" disabled onclick=checkoutuser({{list["uid"]}},1)> Check out </button>
    	% else:
        <br><br><span id="message">You are in a room </span><button id="Checkoutb" type="button" onclick=checkoutuser({{list["uid"]}},1)> Check out </button>

		<br><br><a href="http://localhost:8080/logout"> Logout </a>

		<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
"""

failed_login="""
	The username - {{username}} is already in use please choose another one
	<br><br><a href="http://localhost:8080/">Back to login</a>
"""

notLoggedIn = """
	You are not logged in as a user
	<br><br><a href="http://localhost:8080/">Back to login</a>
"""

login_user_doesnt_exists="""
	The username - {{username}} is does not exist
	<br><br><a href="http://localhost:8080/">Back to login</a>
"""

check_in = """<ol type="1">
	% for id_sala,name in list["rooms"].items():
		<li> {{id_sala}} - {{name}} <button id= "{{id_sala}}" type="button" onclick=checkinuser({{list["id"]}},{{id_sala}},1)> Check in </button>
		<button id ="{{id_sala}}+s" type="button" onclick=listusers({{id_sala}})> Show users </button></li>
	% end

    <br><a href="http://localhost:8080/user">Go Back</a>
</ol>

<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
"""

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
