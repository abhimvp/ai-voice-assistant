# import os
# import uuid
# from livekit import api
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from livekit.api import LiveKitAPI, ListRoomsRequest

# load_dotenv()

# app = FastAPI()

# # Allow all origins to access this
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# async def get_rooms():
#     api = LiveKitAPI()  # Create a new LiveKitAPI instance
#     rooms = await api.room.list_rooms(ListRoomsRequest())  # Lists active rooms
#     await api.aclose()
#     return [room.name for room in rooms.rooms]

# async def generate_room_name():
#     name = "room-" + str(uuid.uuid4())[:8]
#     rooms = await get_rooms()
#     while name in rooms:
#         name = "room-" + str(uuid.uuid4())[:8]
#     return name

# # This is going to issue a new access token which will allow the user to connect to a new room
# @app.get("/getToken")  # allow the user to pass query parameters
# async def get_token(request: Request):
#     name = request.query_params.get("name", "my name")
#     room = request.query_params.get("room", None)

#     if not room:
#         room = await generate_room_name()  # generate a new room name if not provided - random one

#     # get token from livekit  we provide the credentials & identify the user with name & give permissions
#     token = (
#         api.AccessToken(os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET"))
#         .with_identity(name)
#         .with_name(name)
#         .with_grants(api.VideoGrants(room_join=True, room=room))
#     )

#     token_jwt = token.to_jwt()
#     print(f"Generated token: {token_jwt}")  # Debug print to check the token

#     return {"token": token_jwt}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5001, log_level="debug")

import os
from livekit import api
from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
from livekit.api import LiveKitAPI, ListRoomsRequest
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

async def generate_room_name():
    name = "room-" + str(uuid.uuid4())[:8]
    rooms = await get_rooms()
    while name in rooms:
        name = "room-" + str(uuid.uuid4())[:8]
    return name

async def get_rooms():
    api = LiveKitAPI()
    rooms = await api.room.list_rooms(ListRoomsRequest())
    await api.aclose()
    return [room.name for room in rooms.rooms]

@app.route("/getToken")
async def get_token():
    name = request.args.get("name", "my name")
    room = request.args.get("room", None)
    
    if not room:
        room = await generate_room_name()
        
    token = api.AccessToken(os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET")) \
        .with_identity(name)\
        .with_name(name)\
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room
        ))
    
    return token.to_jwt()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)