function isRoomProvided(roomId) {
    console.log('checking id', roomId)

    var url = 'http://localhost:8080/isRoomProvided/' + roomId;

    var xmlObj = new XMLHttpRequest();
    xmlObj.open('GET', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
                console.log('sucesss', xmlObj);
                var jsonResponse = JSON.parse(xmlObj.responseText);
                if (!jsonResponse.roomProvided) {
                    document.getElementById('provideButton').innerHTML = 'Provide room'
                    document.getElementById('provideButton').disabled = false;
                } else {
                    document.getElementById('provideButton').innerHTML = 'Room already provided'
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

    var url = 'http://localhost:8080/provideRoom/' + roomId + '/' + roomName;

    var xmlObj = new XMLHttpRequest();
    xmlObj.open('POST', url, true);
    xmlObj.setRequestHeader("Content-type", "application/json");
    xmlObj.onload = function (e) {
        if (xmlObj.readyState === 4) {
            if (xmlObj.status === 200) {
                console.log('sucesss', xmlObj);
                document.getElementById('provideButton').innerHTML = 'Sucessfully added!'
                document.getElementById('provideButton').disabled = true;
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
