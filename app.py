#!/usr/bin/env python

import asyncio
import websockets
import json
from domaincontroller import DomainController
import uuid


sessions = {}    # dictionary {sessionId: user ID}
active_users = {}    # {user_id: socket}
domaincontroller = DomainController()
counter = 0

async def handler(websocket):
    global counter
    counter += 1
    session_id = str(uuid.uuid4())
    sessions[session_id] = -1
    print(f"\nClient {counter} connected.")
    print("All SESSIONS: ", sessions)

    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosed:
            print(f"Client (({websocket})) disconnected.")
            # izbrisati socket iz active_users{}
            break
        print(f"\nReceived message from Client {websocket}: {message}")
        message_dict = json.loads(message)

        if message_dict["action"] == "signup":
            user = domaincontroller.signup(message_dict["username"], message_dict["password"])
            if domaincontroller.response_ok:
                sessions[session_id] = user["id"]
                print(f"   .....Preparin to sign in {user["username"]}")
                response = {
                    "action": "routing",
                    "url": "http://localhost:8000/chatboard.html?sec="+session_id,
                }
            else:
                print("Not SIGNED UP!")
                response = {
                    "action": "error",
                }
                response["msg"] = "Username already exists" if domaincontroller.code == "user_exists" else "Unknown error"
            print(">>>>Odgovor od servera: ", response)
            await websocket.send(json.dumps(response))

            if domaincontroller.response_ok:
                response = {
                    "action": "new-login",
                    "user": user
                }
                for id, clientsocket in active_users.items():
                    if clientsocket != websocket:
                        print("\n>>>> Odgovor: ", response)
                        await clientsocket.send(json.dumps(response))

        if message_dict["action"] == "login":
            user = domaincontroller.login(message_dict["username"], message_dict["password"])
            if domaincontroller.response_ok:
                sessions[session_id] = user["id"]
                response = {
                    "action": "routing",
                    "url": "http://localhost:8000/chatboard.html?sec="+session_id
                }
            else:
                response = {
                    "action": "error"
                }
                response["msg"] = domaincontroller.code
                print("Odgovor od servera: ", response)

            await websocket.send(json.dumps(response))
            if domaincontroller.response_ok:
                response = {
                    "action": "new-login",
                    "user": user
                }
                for id, clientsocket in active_users.items():
                    if clientsocket != websocket:
                        print("\n>>>> Obavestenje za sve - novi user: ", response)
                        await clientsocket.send(json.dumps(response))

        if message_dict["action"] == "on-load":
            if message_dict["session"] in sessions.keys():
                valid_session_id = message_dict["session"]
                usr_id = sessions[valid_session_id]
                sessions.pop(session_id)    # remove new session_id
                sessions[valid_session_id] = usr_id

                users = domaincontroller.load_users()
                user = domaincontroller.load_user(usr_id)

                active_users[user["id"]] = websocket
                response = {
                    "action": "on-load",
                    "users": users,
                    "user": user
                }
            else:
                response = {"action": "error", "msg": "Session not valid"}
            print(">>>>Odgovor od servera: ", response)
            await websocket.send(json.dumps(response))

        if message_dict["action"] == "logout":
            # change status of the user in DB
            print(">>>> klijent se gasi: ", message_dict)
            deactivated = domaincontroller.deactivate_user(message_dict["userid"])
            if deactivated:
                # destroy session
                del sessions[message_dict["session"]]
                del active_users[message_dict["userid"]]
                print("\n\n>>Aktivne sesije: ", sessions)
                print("Aktivni useri: ", active_users)
                # inform others
                response = {
                    "action": "logout",
                    "userid": message_dict["userid"]
                }
                for socket in active_users.values():
                    print(">>>>Inform everybody GASI SE!!! ==> ", socket)
                    await socket.send(json.dumps(response))

        if message_dict["action"] == "load-friend":
            print("\n>>>> OD CLIENT-a load-friend: ", message_dict)
            if message_dict["session"] in sessions:
                user = domaincontroller.load_user(message_dict["userid"])
                # messages = domaincontroller.load_messages(message_dict["userid"])
                if domaincontroller.response_ok:
                    response = {
                        "action": "load-friend",
                        "user": user,
                        "messages": "messages - to be developed"
                    }
                else:
                    response = {"action": "error", "msg": domaincontroller.code}
            else:
                response = {"action": "error", "msg": "Session not valid"}
            await websocket.send(json.dumps(response))

        if message_dict["action"] == "message-sent":
            # current websocket is sending message to a friend
            print("\n>>>> OD CLIENT-b message :: ", message_dict)
            if message_dict["session"] in sessions:
                sgn = domaincontroller.received_message(message_dict["from"],
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


if __name__ == "__main__":
    asyncio.run(main())