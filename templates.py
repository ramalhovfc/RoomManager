index = '''
    	<h2>Welcome to Room Management</h2>
    	<form action="/" method="post">
    		Username: <input name="username" type="text" /><br><br>
    		<button type="submit" formaction="/login">Login</button>
			<button type="submit" formaction="/signin">Signin</button>
    	</form>
'''

temp_adminArea = """
	<h2>Administrator Area</h2>
	<ol type="1">
		<li><a href="http://localhost:8080/admin/spaces">Search spaces</a></li>
		<li><a href="http://localhost:8080/admin/roomsOcupancy">List room ocupancy</a></li>
	</ol>
"""

temp_roomsOcupancy = """
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
"""

temp_spaces = """
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
</ol>"""

logged_in = """
	<br><a href="http://localhost:8080/user/rooms">List Available Rooms</a>

	<br><br>You currently are in room <button id="Checkoutb" type="button" onclick=checkoutuser({{uid}})> Check out </button>
	<div id='provideButton'>
	<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
"""

temp_failed_login="""
	The username - {{username}} is already in use please choose another one
	<br><br><a href="http://localhost:8080/">Back to login</a>
"""

temp_login_user_doesnt_exists="""
	The username - {{username}} is does not exist
	<br><br><a href="http://localhost:8080/">Back to login</a>
"""

temp = """
<ol type="1">
	% for id_sala, name in list["rooms"].items():
		<li> {{id_sala}} - {{name}}
			<button id="{{id_sala}}" type="button" onclick=checkinuser({{list["id"]}},{{id_sala}})> Check in </button>
			<button type="button" onclick=listusers({{id_sala}})> Show users </button>
		</li>
	% end
</ol>

<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
"""

temp_provide = """
<ol>
	Type : {{list["type"]}} <br>
	Name : {{list["name"]}} <br>
	Campus : {{list["parentSpace"]["topLevelSpace"]["name"]}}<br> <br>

	<button id="provideButton" onclick="provideRoom({{list["id"]}}, \'{{list["name"]}}\')" disabled	>Checking if room is already provided...</button>

	<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}" ></script>
	<script type="text/javascript"> isRoomProvided({{list["id"]}}) </script>
</ol>"""

temp_utilizadores= """
	% for id, name in list.items():
		{{id}}:{{name}}
	% end
"""
