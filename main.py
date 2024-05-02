#!/usr/bin/env python

import asyncio
import websockets
import json
from controller import Controller
import uuid


sessions = {}    # dictionary {sessionId: user ID}
active_users = {}    # {user_id: socket}
controller = Controller()
counter = 0  # counts the number of websockets created - for control purposes
current_user = None

async def handler(websocket):
    global counter
    counter += 1
    session_id = str(uuid.uuid4())
    sessions[session_id] = -1

    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosed:
            print(f"Client (({websocket})) disconnected.")
            break

        message_dict = json.loads(message)

        if message_dict["action"] == "signup":
            user = controller.signup(message_dict["username"], message_dict["password"])
            if controller.response_ok:
                sessions[session_id] = user["id"]

                response = {
                    "action": "routing",
                    "url": "http://localhost:8000/chatboard.html?sec="+session_id,
                }
            else:
                response = {
                    "action": "error",
                }
                response["msg"] = controller.code
            await websocket.send(json.dumps(response))

            if controller.response_ok:
                response = {
                    "action": "new-login",
                    "user": user
                }
                for id, clientsocket in active_users.items():
                    if clientsocket != websocket:
                        await clientsocket.send(json.dumps(response))

        if message_dict["action"] == "login":
            user = controller.login(message_dict["username"], message_dict["password"])
            if controller.response_ok:
                sessions[session_id] = user["id"]
                response = {
                    "action": "routing",
                    "url": "http://localhost:8000/chatboard.html?sec="+session_id
                }
            else:
                response = {
                    "action": "error"
                }
                response["msg"] = controller.code

            await websocket.send(json.dumps(response))
            if controller.response_ok:
                response = {
                    "action": "new-login",
                    "user": user
                }
                for id, clientsocket in active_users.items():
                    # inform all users that new user logged in
                    if clientsocket != websocket:
                        await clientsocket.send(json.dumps(response))

        if message_dict["action"] == "on-load":
            if message_dict["session"] in sessions.keys():
                valid_session_id = message_dict["session"] # we will use the "old" session created before sign in
                usr_id = sessions[valid_session_id]
                sessions.pop(session_id)    # remove new session_id
                sessions[valid_session_id] = usr_id

                users = controller.load_users()
                current_user = controller.load_user(usr_id)

                active_users[current_user["id"]] = websocket
                response = {
                    "action": "on-load",
                    "users": users,
                    "user": current_user
                }
            else:
                response = {"action": "error", "msg": "Session not valid"}
            await websocket.send(json.dumps(response))

        if message_dict["action"] == "logout":
            # change status of the user in DB
            deactivated = controller.logout(message_dict["userid"])
            if deactivated:
                # destroy session
                del sessions[message_dict["session"]]
                del active_users[message_dict["userid"]]

                # inform others
                response = {
                    "action": "logout",
                    "userid": message_dict["userid"]
                }
                for socket in active_users.values():
                    await socket.send(json.dumps(response))

        if message_dict["action"] == "load-friend":
            if message_dict["session"] in sessions:
                response = {}
                # fill the response with friend's data
                if load_user(message_dict["userid"], response):
                    # add conversation messages with the friend
                    sgn = load_conversation(message_dict["userid"], message_dict["current_id"], response)
            else:
                response = {"action": "error", "msg": "Session not valid"}
            await websocket.send(json.dumps(response))

        if message_dict["action"] == "message-sent":
            # current websocket is sending message to a friend
            if message_dict["session"] in sessions:
                sgn = controller.received_message(message_dict["from"],
                                                        message_dict["to"],
                                                        message_dict["message"])
                if message_dict["to"] in active_users:
                    # if recipient in active_users
                    socket = active_users[message_dict["to"]]
                    if sgn:
                        # and if message saved in DB, forward message to the recipient and inform sender of success
                        forward_response = {
                            "action": "message-received",
                            "from_id": message_dict["from"],
                            "message": message_dict["message"],
                        }
                        response = {
                            "action": "receipt-confirmation",
                            "success": "success",
                            "message": message_dict["message"]
                        }
                        await socket.send(json.dumps(forward_response))
                    else:
                        # inform sender of failure to send (save msg in DB)
                        response = {
                            "action": "receipt-confirmation",
                            "success": "fail",
                            "message": message_dict["message"]
                        }
                else:
                    if sgn:
                        # recipient not online, but message successfuly saved
                        response = {
                            "action": "receipt-confirmation",
                            "success": "will be delivered later",
                            "message": message_dict["message"]
                        }
            else:
                response = {"action": "error", "msg": "Session not valid"}
            await websocket.send(json.dumps(response))

        if message_dict["action"] == "message":
            for id, socket in active_users.items():
                if id != user_id:
                    await socket.send(json.dumps(message_dict))


async def main():
    async with websockets.serve(handler, "", 8022):
        await asyncio.Future()  # run forever


def load_user(user_id: int, response: dict) -> bool:
    user = controller.load_user(user_id)
    # messages = controller.load_messages(message_dict["userid"])
    if controller.response_ok:
        response["action"] = "load-friend"
        response["user"] = user
        return True
    else:
        response = {"action": "error", "msg": controller.code}
        return False

def load_conversation(user_id: int, current_id: int, response: dict) -> bool:
    # load the conversation between current user and requested id
    msg_dict = controller.load_conversation(current_id, user_id)
    if controller.response_ok:
        response["conversation"] = msg_dict
        return True
    else:
        response = {"action": "error", "msg": controller.code}
    return False


if __name__ == "__main__":
    asyncio.run(main())