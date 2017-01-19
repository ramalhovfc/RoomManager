index = '''
    	<h2>Welcome to Room Management</h2>
    	<form action="/" method="post">
    		Username: <input name="username" type="text" /><br>
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

temp_spaces = """<ol type="1">
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
		<br><a href="http://localhost:8080/user/{{uid}}/rooms">List Available Rooms</a>

    	<br><br>You currently are in room <button id="Checkoutb" type="button" onclick=checkoutuser({{uid}})> Check out </button>
    	<div id='provideButton'>
<script>
function checkoutuser(uid) {

    var url = 'http://localhost:8080/api/checkout';
    var userid = {uid: uid}

    var xmlObj = new XMLHttpRequest();
    xmlObj.open('POST', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
            	var exemplo=JSON.parse(xmlObj.responseText)
            	if (exemplo["state"]==0){
            		alert("you are not checked in")
            	}else{
            		alert("you were checked out")
            	}

                document.getElementById('Checkoutb').disabled = true;
            } else {
                document.getElementById('Checkoutb').innerHTML = 'Something went wrong:' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };
    xmlObj.onprogress = function (e) {
        document.getElementById('Checkoutb').innerHTML += '.'
    }
    xmlObj.onerror =
    function (e) {
        document.getElementById('Checkoutb').innerHTML = 'Something went wrong:' + e.statusText;
        console.error(e);
    };

    xmlObj.send(JSON.stringify(userid));
}
</script>
"""

temp_failed_login="""
		The username - {{username}} is already in use please choose another one
		<br><br><a href="http://localhost:8080/">Back to login</a>
"""

temp_login_user_doesnt_exists="""
		The username - {{username}} is does not exist
		<br><br><a href="http://localhost:8080/">Back to login</a>
"""

temp = """<ol type="1">
	% for id_sala,name in list["rooms"].items():
		<li> {{id_sala}} - {{name}} <button id= "{{id_sala}}" type="button" onclick=checkinuser({{list["id"]}},{{id_sala}})> Check in </button>
		<button type="button" onclick=listusers({{id_sala}})> Show users </button></li>
	% end

	//fazer div para mostrar template
</ol>

<script>
function listusers(id_sala){
	alert("lista de utilzadores logados");
	/*var url = 'http://localhost:8080/api/listusers/'+id_sala;
	//window.location.href= url
	var xhttp = new XMLHttpRequest();
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();*/
    var url = 'http://localhost:8080/api/listusers/'+id_sala;
    var xmlObj = new XMLHttpRequest();
    xmlObj.open('GET', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
            	var exemplo=JSON.parse(xmlObj.responseText)
            	if (exemplo["state"]== 0){
            		alert("The room has no users");
            	}else{
            		alert(JSON.stringify(exemplo["users"]));
            	}
            	//window.location.href= url
                //document.getElementById(id_sala).disabled = true;
            } else {
                document.getElementById(id_sala).innerHTML = 'Something went wrong:' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };
    xmlObj.onprogress = function (e) {
        document.getElementById(id_sala).innerHTML += '.'
    }
    xmlObj.onerror = function (e) {
        document.getElementById(id_sala).innerHTML = 'Something went wrong:' + e.statusText;
        console.error(e);
    };
    xmlObj.send();
}
function checkoutuser(uid) {

    var url = 'http://localhost:8080/api/checkout';
    var userid = {uid: uid}

    var xmlObj = new XMLHttpRequest();
    xmlObj.open('POST', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
            	var exemplo=JSON.parse(xmlObj.responseText)
            	if (exemplo["state"]==0){
            		alert("you are not checked in")
            	}else{
            		alert("you were checked out")
            	}

                document.getElementById('Checkoutb').disabled = true;
            } else {
                document.getElementById('Checkoutb').innerHTML = 'Something went wrong:' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };
    xmlObj.onprogress = function (e) {
        document.getElementById('Checkoutb').innerHTML += '.'
    }
    xmlObj.onerror =
    function (e) {
        document.getElementById('Checkoutb').innerHTML = 'Something went wrong:' + e.statusText;
        console.error(e);
    };

    xmlObj.send(JSON.stringify(userid));
}
function checkinuser(usid ,idr) {
    var url = 'http://localhost:8080/api/checkin';
    var data = {uid: usid, roomid: idr};
    var xmlObj = new XMLHttpRequest();
    xmlObj.open('POST', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
            	var exemplo=JSON.parse(xmlObj.responseText)
            	if (exemplo["state"]==1){
            		alert("you are now checked in")
            		document.getElementById(idr).innerHTML = 'Sucessfully added!'
            		//document.getElementById(idr).disabled = true;
            	}else if(exemplo["state"]==-1){
            		alert("You are already in this room")
            	}else{
            		alert("You are already in a room")
            		checkoutuser(usid)
            		alert("You are in a new room now")
            		checkinuser(usid, idr)
            	}
            } else {
                document.getElementById(idr).innerHTML = 'Something went wrong:' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };
    /*xmlObj.onprogress = function (e) {
        document.getElementById(idr).innerHTML += '.'
    }*/
    xmlObj.onerror = function (e) {
        document.getElementById(idr).innerHTML = 'Something went wrong:' + e.statusText;
        console.error(e);
    };
    xmlObj.send(JSON.stringify(data));
}
</script>
"""

temp_provide = """
<ol>
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
