index = '''
    	Welcome to Room Management

    	<form action="/" method="post">
    		<br>Username: <input name="username" type="text" /><br><br>
    		<input value="Login" type="submit" />
    	</form>
    '''

index2 = '''
	<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}"></script>
	Welcome to Room Management
	<form action="javascript:;" onsubmit="login(this)">
		Username: <input name="username" type="text" /><br><br>
		<input value="Login" type="submit" />
	</form>
	<div id="errorDiv" style="color:red" />
'''

temp_spaces = """<ol type="1">
	% if (list[0]["type"] == "FLOOR"):
		Floors 	<br><br>
	%end
	% for a in list:
		% if (a["name"] == ""):
			<li><a href="http://localhost:8080/0/space/{{a["id"]}}"> {{a["id"]}} </a></li>
		% else:
			<li><a href="http://localhost:8080/0/space/{{a["id"]}}"> {{a["name"]}} </a></li>
		%end
	% end
</ol>"""

logged_in = """

		<br><a href="http://localhost:8080/user/{{uid}}/rooms">List Available Rooms</a>

    	<br><br>You currently are in room <button type="button" onclick=checkoutuser()> Check out </button>


"""
"""
<script>
function checkoutuser(idr) {
	var xhttp = new XMLHttpRequest();
	xhttp.open("POST", "http://localhost:8080/api/checkin", true);
	xhttp.send("uid={{list["id"]}}&roomid="+idr);
	alert('checked out')
}
</script>
"""

temp_failed_login="""
		The username - {{username}} is already in use please choose another one

		<br><br><a href="http://localhost:8080/">Back to login</a>
"""

temp = """<ol type="1">

	% for a,b in list["rooms"].items():
		<li> {{a}} - {{b}} <button type="button" onclick=checkinuser({{a}})> Check in </button> </li>
	% end
</ol>

<script>
function checkinuser(idr) {
	var xhttp = new XMLHttpRequest();
	xhttp.open("POST", "http://localhost:8080/api/checkin", true);
	xhttp.send("uid={{list["id"]}}&roomid="+idr);
	alert(idr)
}
</script>
"""

temp_provide = """<ol>
	Type : {{list["type"]}} <br>
	Name : {{list["name"]}} <br>
	Campus : {{list["parentSpace"]["topLevelSpace"]["name"]}}<br> <br>

	<button id="provideButton" onclick="provideRoom({{list["id"]}}, \'{{list["name"]}}\')" disabled	>Checking if room is already provided...</button>

	<script type="text/javascript" src="{{ get_url('static', filename='main.js') }}"></script>
	<script type="text/javascript"> isRoomProvided({{list["id"]}}) </script>
</ol>"""

temp_utilizadores= """
	% for id, name in list.items():
		{{id}}:{{name}}
	% end
"""
