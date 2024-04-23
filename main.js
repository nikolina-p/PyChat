
window.addEventListener("DOMContentLoaded", () => {
  // Open the WebSocket connection and register event handlers.
  const websocket = new WebSocket("ws://localhost:8022/");
  websocket.addEventListener("open", () => {
    var searchParams = new URLSearchParams(window.location.search);
    var secValue = searchParams.get('sec');

    window.user = {
      id: -1,
      username: -1,
      session: secValue,
      socket: websocket,
      talkig_to: -1
    };

    const login = {
      action: "on-load",
      session: secValue
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

      case "load-friend":
        console.log("LOAD FRIEND:: " + message.user.id + " " + message.user.username+ " " + message.user.active)
        window.user.talkig_to = message.user.id
        renderTalkingTo(message.user);
        renderConversation(message.conversation)
        break;

      case "message-received":
        console.log("NEW MESSAGE: " + message.from_id + " " + message.message)
        // if user is in talking-to (chat with him/her is open), just append message to te message board
        if (window.user.talkig_to === message.from_id) {
          addMessage(false, message.message)
        } else {
          // if user is not in talking-to, make the sender blue and add blie dot and maybe small popup "new message"
          addNewMessageIndicator(message.from_id)
        }
        break;

      case "receipt-confirmation":
        if (message.success == "success") {
          addMessage(true, message.message);
        }
        break;

      case "load-conversation":
        let conversation = message.conversation
        console.print(conversation)
    }
  });
}

function sendMessages(websocket) {
  var sendBtt = document.getElementById("sendbtt")

  sendBtt.addEventListener("click", () => {
    console.log("Button clicked")

    let myTextArea = document.getElementById("typing")
    let msg = myTextArea.value
    myTextArea.value = ""

    let response = {
      action: "message-sent",
      session: window.user.session,
      from: window.user.id,
      to: window.user.talkig_to,
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

  const messageContainer = document.createElement("div");
  messageContainer.classList.add("message-container");

  const messageElement = document.createElement("li");

  messageElement.textContent = text;
  messageElement.classList.add("message");
  if (isSent) {
    messageElement.classList.add("sent");
  } else {
    messageElement.classList.add("received");
  }
  messageContainer.appendChild(messageElement); // Append the li to the div
  messagesList.appendChild(messageContainer);

  // Add a line break after each message
  const lineBreak = document.createElement("br");
  messagesList.appendChild(lineBreak);
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
    console.log('Clicked on user:', user);

    let response = {
      "action": "load-friend",
      "session": window.user.session,
      "userid": user.id,
      "current_id": window.user.id
    }

    window.user.socket.send(JSON.stringify(response));
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

function renderTalkingTo(user) {
  let div = document.getElementById("talking-to")
  div.innerText = user.username + " :: "

  let typingTextarea = document.getElementById("typing")

  if (user.active == 0) {
    textareaFriendNotActive(typingTextarea)
  }

  let userDiv = document.getElementById(user.id)
  // remove new-message-indicator
  userDiv.innerHTML = ""
  userDiv.innerText = user.username
}

function textareaFriendNotActive(typingTextarea) {
    // inform the user that friend is not active
    var inactiveFriend = "The user is not active at the moment. They might not see your message imediatelly..."
    typingTextarea.value = inactiveFriend;
    typingTextarea.style.color = '#999';
    typingTextarea.style.fontStyle = 'italic';

    typingTextarea.addEventListener('focus', function() {
        // Clear the textarea when it gains focus if it contains the default text
        if (typingTextarea.value === inactiveFriend) {
            typingTextarea.value = '';
            typingTextarea.style.color = '';
            typingTextarea.style.fontStyle = '';
        }
    });

    typingTextarea.addEventListener('blur', function() {
      // do the same thing when textarea again loses focus
        if (typingTextarea.value === '') {
            typingTextarea.value = inactiveFriend;
            typingTextarea.style.color = '#999';
            typingTextarea.style.fontStyle = 'italic';
        }
    });
}

function addNewMessageIndicator(id) {
  console.log("ID div sender: "+id);
    // Make sender blue
    var targetDiv = document.getElementById(id);
    targetDiv.style.color = '#87b5fa'

    var newMessageIndicator = document.createElement("span");
    newMessageIndicator.textContent = "New message";
    newMessageIndicator.classList.add("new-message-indicator");

    // Append the new message indicator next to the div's text
    targetDiv.appendChild(newMessageIndicator);
}

function renderConversation(conversation) {
  const messagesList = document.getElementById("messages-list");
  messagesList.innerHTML = " "

  for (let key in conversation) {
    if (conversation.hasOwnProperty(key)) {
      const msg = conversation[key];
      let sgn = true
      if (msg[1] !== window.user.id) {
        // if the message is received
        sgn = false
      }
      addMessage(sgn, msg[3])
    }
  }
}
