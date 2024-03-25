
window.addEventListener("DOMContentLoaded", () => {
  // Open the WebSocket connection and register event handlers.
  const websocket = new WebSocket("ws://localhost:8022/");
  websocket.addEventListener("open", () => {
    var searchParams = new URLSearchParams(window.location.search);
    var secValue = searchParams.get('sec');

    window.user = {
      id: -1,
      username: -1,
      session: secValue
    };

    const login = {
      action: "on-load",
      secret: secValue
    };
    websocket.send(JSON.stringify(login));
  });

  receiveMessages(websocket);
  sendMessages(websocket);
  windowClose(websocket)
});

function receiveMessages(websocket) {
  websocket.addEventListener("message", ({ data }) => {
    let message = JSON.parse(data);
    console.log(message)

    switch (message.action){
      // SWITCH CASE HERE I AM
      case "on-load":
        renderUser(message.user)
        renderUserList(message.users, message.user);
        break;

      case "new-login":
        console.log("NEW USER LOGEDIN"+message);
        var user = message.user;
        if (document.getElementById(user.id)) {
          activateUser(user.id, true);
        } else {
          appendUser(document.getElementById("userlist"), user);
        }
        break;

      case "logout":
        console.log("USER LOGGED OUT "+ message.userid)
        activateUser(message.userid, false)
        break;
    }
  });
}

function sendMessages(websocket) {
  var sendBtt = document.getElementById("sendbtt")

  sendBtt.addEventListener("click", () => {
    console.log("Button clicked")

    let myTextArea = document.getElementById("typing")
    let msg = myTextArea.value
    myTextArea.innerText = " "
    myTextArea.innerHTML = " "
    myTextArea.value = " "

    let username = document.getElementById("username").innerText

    let response = {
      id: username,
      message: msg
    };
    console.log("Mgs:", msg)
    websocket.send(JSON.stringify(response));
  });
}

function windowClose(websocket) {
  window.addEventListener( "beforeunload", () => {
    console.log("beforeunload ::  window.user.id = "+window.user.id)
    if (window.user.id != -1){
      var response = {
      action: 'logout',
      session: window.user.session,
      userid: window.user.id
      }
      websocket.send(JSON.stringify(response));
    }


  })
}
function addMessage(isSent, text) {
  const messagesList = document.getElementById("messages-list");
  const messageElement = document.createElement("li");
  messageElement.textContent = text;
  messageElement.classList.add("message");
  if (isSent) {
    messageElement.classList.add("sent");
  } else {
    messageElement.classList.add("received");
  }
  messagesList.appendChild(messageElement);
}

function renderUser(user) {
  console.log("USER: "+user)
  window.user.id = user.id;
  window.user.username = user.username

  document.getElementById("my-name").innerText = "Hi, " + user.username
  let img = user.id % 3

  document.getElementById("my-photo").innerHTML = '<img src=\"img/'+ img +'.jpg\" alt=\"profile-photo\">'
}

function renderUserList(users, user) {
  const userlistDiv = document.getElementById('userlist');
  userlistDiv.innerHTML = '';

  for (let key in users) {
    if (users.hasOwnProperty(key)) {
      const item = users[key];

      if (user.id != item.id) {
        appendUser(userlistDiv, item);
      }
    }
  }
}

function appendUser(userlistDiv, user) {
  const userDiv = document.createElement('div');
  userDiv.classList.add('user');
  if (user.active == "0") {
        userDiv.classList.add('inactive')
      }
  userDiv.id = user.id
  userDiv.textContent = user.username;

      // Add click event listener to each user element
  userDiv.addEventListener('click', () => {
        // Do something when user is clicked
    console.log('Clicked on user:', user);
  });

  userlistDiv.appendChild(userDiv);

  console.log(user.id + " " + user.username);
}

/*function removeUser(message) {
  let userDiv = document.getElementById(message.userid)
  userDiv.remove()
}*/

function activateUser(id, active) {
  if (id != null) {
    var userDiv = document.getElementById(id)

    if (active == true) {
      userDiv.classList.remove('inactive');
    } else {
      userDiv.classList.add('inactive');
    }
  }
}
