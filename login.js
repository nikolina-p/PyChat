
window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8022/");

    login(websocket)
    signup(websocket)
    receiveMessages(websocket)
})

function login(websocket) {
    var loginBtt = document.getElementById('login')

    loginBtt.addEventListener('click', () => {
        var username = document.getElementById('username').value
        var password = document.getElementById('password').value
        console.log("Login clicked")

        var jsonMsg = {
            action: "login",
            username: username,
            password: password
        }
        websocket.send(JSON.stringify(jsonMsg))
    })
}

function signup(websocket) {
    var signupBtt = document.getElementById('signup')

    signupBtt.addEventListener('click', () => {
        var username = document.getElementById('username').value
        var password = document.getElementById('password').value

        var jsonMsg = {
            action: "signup",
            username: username,
            password: password
        }
        websocket.send(JSON.stringify(jsonMsg))
    })
}

function receiveMessages(websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const message = JSON.parse(data);
    console.log(message)
    var user = message.user
    if (message.action == "routing") {
        console.log(message)
        var url = message.url
        window.location.href = url
    }
    else if (message.action == "error") {
        console.log(message.msg)
        var err = document.getElementById("error")
        err.textContent = message.msg
    }
  });
}
