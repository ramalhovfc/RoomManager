function isRoomProvided(roomId) {
    console.log('checking id', roomId)

    var url = 'http://' + document.roomManager.serverHost + document.roomManager.serverPort + '/admin/spaces/provided/' + roomId;

    var xmlObj = new XMLHttpRequest();
    xmlObj.open('GET', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
                console.log('sucesss', xmlObj);
                var jsonResponse = JSON.parse(xmlObj.responseText);
                if (!jsonResponse.roomProvided) {
                    document.getElementById('provideButton').innerHTML = 'Add'
                    document.getElementById('provideButton').disabled = false;
                } else {
                    document.getElementById('provideButton').innerHTML = 'Room already provided'
                    document.getElementById('deleteButton').disabled = false
                }
            } else {
                document.getElementById('provideButton').innerHTML = 'Something went wrong: ' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };
    xmlObj.onprogress = function (e) {
        document.getElementById('provideButton').innerHTML += '.'
    }
    xmlObj.onerror = function (e) {
        document.getElementById('provideButton').innerHTML = 'Something went wrong: ' + e.statusText;
        console.error(e);
    };

    xmlObj.send();
}

function provideRoom(roomId, roomName) {
    if (!roomName) {
        roomName = '<no-name>'
    }
	console.log('providing id', roomId)
	console.log('providing name', roomName)

    var url = 'http://' + document.roomManager.serverHost + document.roomManager.serverPort + '/api/spaces/provide/' + roomId + '/' + roomName;

    var xmlObj = new XMLHttpRequest();
    xmlObj.open('POST', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
                console.log('sucesss', xmlObj);
                document.getElementById('provideButton').innerHTML = 'Sucessfully added!'
                document.getElementById('provideButton').disabled = true;
                document.getElementById('deleteButton').innerHTML = 'Delete';
                document.getElementById('deleteButton').disabled = false;
            } else {
                document.getElementById('provideButton').innerHTML = 'Something went wrong: ' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };
    xmlObj.onprogress = function (e) {
        document.getElementById('provideButton').innerHTML += '.'
    }
    xmlObj.onerror = function (e) {
        document.getElementById('provideButton').innerHTML = 'Something went wrong: ' + e.statusText;
        console.error(e);
    };

    document.getElementById('provideButton').innerHTML = 'Adding...'
    xmlObj.send();
}

function deleteRoom(roomId) {
    var url = 'http://' + document.roomManager.serverHost + document.roomManager.serverPort + '/api/spaces/provide/' + roomId;

    var xmlObj = new XMLHttpRequest();
    xmlObj.open('DELETE', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
                console.log('sucesss', xmlObj);
                document.getElementById('deleteButton').innerHTML = 'Sucessfully deleted!'
                document.getElementById('deleteButton').disabled = true;
                document.getElementById('provideButton').disabled = false;
                document.getElementById('provideButton').innerHTML = 'Add';
            } else {
                document.getElementById('deleteButton').innerHTML = 'Something went wrong: ' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };
    xmlObj.onprogress = function (e) {
        document.getElementById('deleteButton').innerHTML += '.'
    }
    xmlObj.onerror = function (e) {
        document.getElementById('deleteButton').innerHTML = 'Something went wrong: ' + e.statusText;
        console.error(e);
    };

    document.getElementById('deleteButton').innerHTML = 'Deleting...'
    xmlObj.send();
}

function listusers(id_sala){
    var url = 'http://' + document.roomManager.serverHost + document.roomManager.serverPort + '/api/listusers/' + id_sala;

    var xmlObj = new XMLHttpRequest();
    xmlObj.open('GET', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
            	var exemplo=JSON.parse(xmlObj.responseText)
            	if (exemplo["state"] === 404){
            		alert("The room has no users");
            	} else {
                    var users = []
                    for (var key in exemplo["users"]){
                        users.push(exemplo["users"][key])
                    }
                    alert(users)
            	}
            } else {
                document.getElementById(id_sala+s).innerHTML = 'Something went wrong:' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };
    xmlObj.onerror = function (e) {
        document.getElementById(id_sala+s).innerHTML = 'Something went wrong:' + e.statusText;
        console.error(e);
    };
    xmlObj.send();
}
function checkoutuser(uid, message) {
    var checkoutButton = document.getElementById('Checkoutb');
    var url = 'http://' + document.roomManager.serverHost + document.roomManager.serverPort + '/api/checkout';
    var userid = {uid: uid}

    var xmlObj = new XMLHttpRequest();
    xmlObj.open('PUT', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
            	var exemplo=JSON.parse(xmlObj.responseText)
            	if (exemplo["state"] === 404 && message === 1) {
            		alert("you are not checked in")
            	} else if(message === 1){
   	                document.getElementById('message').innerHTML = 'You are not in a room '
            		alert("you were checked out")
            	}

                if (checkoutButton)
                    checkoutButton.disabled = true;
            } else {
                if (checkoutButton)
                    document.getElementById('Checkoutb').innerHTML = 'Something went wrong:' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };

    xmlObj.onerror = function (e) {
        if (checkoutButton)
            document.getElementById('Checkoutb').innerHTML = 'Something went wrong:' + e.statusText;
        console.error(e);
    };

    xmlObj.send(JSON.stringify(userid));
}
function checkinuser(usid ,idr, message) {
    var url = 'http://' + document.roomManager.serverHost + document.roomManager.serverPort + '/api/checkin';
    var data = {uid: usid, roomid: idr};
    var xmlObj = new XMLHttpRequest();
    xmlObj.open('PUT', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
            	var exemplo = JSON.parse(xmlObj.responseText)
            	if (exemplo["state"] === 201){
            		if (message === 1){
                        alert("you are now checked in")
                    }
            	}else if(exemplo["state"] === 400){
            		alert("You are already in this room")
            	}else if (exemplo["state"]==200){
                    alert("You are now in a different room")
            	}
            } else {
                document.getElementById(idr).innerHTML = 'Something went wrong:' + xmlObj.statusText;
                console.error(xmlObj);
            }
        }
    };
    xmlObj.onerror = function (e) {
        document.getElementById(idr).innerHTML = 'Something went wrong:' + e.statusText;
        console.error(e);
    };
    xmlObj.send(JSON.stringify(data));
}
