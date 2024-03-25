#!/usr/bin/env python

import asyncio
import websockets
import json
from domaincontroller import DomainController
import uuid

# dictionary {sessionId: (websocket, userid)}
sessions = {}
# {user_id: socket}
active_users = {}
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
            if message_dict["secret"] in sessions.keys():
                valid_session_id = message_dict["secret"]
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

        if message_dict["action"] == "message":
            for id, socket in active_users.items():
                if id != user_id:
                    await socket.send(json.dumps(message_dict))


async def main():
    async with websockets.serve(handler, "", 8022):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())