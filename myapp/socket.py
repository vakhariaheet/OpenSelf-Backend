import socketio
# from utils import config
import json
from django.shortcuts import get_object_or_404
from .models import User, ChatMessage
# from .models import Chat, ChatMessage
# from .serializers import MessageSerializer
from asgiref.sync import sync_to_async

mgr = socketio.AsyncRedisManager("redis://localhost:6379")
sio = socketio.AsyncServer(
    async_mode="asgi", client_manager=mgr, cors_allowed_origins="*"
)


USER_SOCKET_MAP = {}

# establishes a connection with the client
@sio.on("connect")
async def connect(sid, env, auth):
    print("SocketIO connect")   


@sio.on("join")   
async def join(sid, data):   
    id = data["id"]      
    USER_SOCKET_MAP[id] = sid
    print("SocketIO join", sid, data)     
    await sio.emit("join", f"Joined as {sid}", to=sid)
    

# communication with orm
def store_and_return_message(data):
    if isinstance(data, str):
        data = json.loads(data)
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    text = data["text"]
    sender = get_object_or_404(User, pk=sender_id)
    receiver = get_object_or_404(User, pk=receiver_id)
    # # chat = get_object_or_404(Chat, short_id=chat_id)

    instance = ChatMessage.objects.create(sender=sender,receiver=receiver, text=text)
    instance.save()
    return data


# listening to a 'message' event from the client
@sio.on("message")
async def print_message(sid, data):
    print("Socket ID", sid)
    message = await sync_to_async(store_and_return_message,  thread_sensitive=True)(
        data
    )  # communicating with orm
    print(USER_SOCKET_MAP[message["receiver_id"]])
    await sio.emit("new_message", message, to=USER_SOCKET_MAP[message["receiver_id"]])# sending the message back to the client

