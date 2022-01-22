from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.core.serializers import serialize

import json

from directmessage.models import Message, DirectMessageRoom
from account.utils import LazyAccountEncoder

from directmessage.exceptions import ClientError

from directmessage.utils import calculate_timestamp
from django.utils import timezone

from directmessage.constants import *

class ChatConsumer(AsyncJsonWebsocketConsumer):


    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        print("ChatConsumer: connect: " + str(self.scope["user"]))

        # let everyone connect. But limit read/write to authenticated users
        await self.accept()

        # the room_id will define what it means to be "connected". If it is not None, then the user is connected.
        self.room_id = None


    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        print("ChatConsumer: receive_json")
        command = content.get("command", None)
        try:
            if command == "join":
                print("joining room: " + str(content['room']))
                await self.join_room(content['room'])
            elif command == "leave":
                await self.leave_room(content["room"])
            elif command == "send":
                if len(content["message"].lstrip()) != 0:
                    await self.send_room(content["room"], content["message"])
            elif command == "get_room_chat_messages":
                pass
            elif command == "get_user_info":
                room = await get_room_or_error(content['room_id'], self.scope["user"])
                payload= await get_user_info(room, self.scope["user"])
                if payload != None:
                    payload=json.loads(payload)
                    await self.send_user_info_payload(payload['user_info'])
                else:
                    raise ClientError(204, "Something went wrong retrieving the other users account details.")

        except ClientError as e:
            await self.handle_client_error(e)


    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave the room
        print("ChatConsumer: disconnect")
        try:
            if self.room_id != None:
                await self.leave_room(self.room_id)
        except Exception as e:
            print("EXCEPTION: " + str(e))
            pass


    async def join_room(self, room_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware (AuthMiddlewareStack)
        print("ChatConsumer: join_room: " + str(room_id))
        try:
            room = await get_room_or_error(room_id, self.scope['user'])
        except ClientError as e:
            return await self.handle_client_error(e)

         # Store that we're in the room
        self.room_id = room.id

        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )


        # Instruct their client to finish opening the room
        await self.send_json({
            "join": str(room.id),
        })


    async def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        print("ChatConsumer: leave_room")

        room = await get_room_or_error(room_id, self.scope["user"])

        # Notify the group that someone left
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.leave",
                "room_id": room_id,
                "profile_image": self.scope["user"].profile_image.url,
                "username": self.scope["user"].username,
                "user_id": self.scope["user"].id,
            }
        )

        # Remove that we're in the room
        self.room_id = None

        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the room
        await self.send_json({
            "leave": str(room.id),
        })




    async def send_room(self, room_id, message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        print("ChatConsumer: send_room")
        # Check they are in this room
        if self.room_id != None:
            if str(room_id) != str(self.room_id):
                raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
        else:
            raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")

        # Get the room and send to the group about it
        room = await get_room_or_error(room_id, self.scope["user"])

        await create_room_chat_message(room, self.scope["user"], message)

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message", #chat_message
                "profile_image": self.scope["user"].profile_image.url,
                "username": self.scope["user"].username,
                "user_id": self.scope["user"].id,
                "message": message,
            }
        )


    # These helper methods are named by the types we send - so chat.join becomes chat_join
    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        print("ChatConsumer: chat_join: " + str(self.scope["user"].id))


    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        print("ChatConsumer: chat_leave")


    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        print("ChatConsumer: chat_message")

        timestamp = calculate_timestamp(timezone.now())

        await self.send_json(
            {
                "msg_type": MSG_TYPE_MESSAGE,
                "username": event["username"],
                "user_id": event["user_id"],
                "profile_image": event["profile_image"],
                "message": event["message"],
                "natural_timestamp": timestamp,
            },
        )


    async def send_messages_payload(self, messages, new_page_number):
        """
        Send a payload of messages to the ui
        """
        print("ChatConsumer: send_messages_payload. ")


    async def send_user_info_payload(self, user_info):
        """
        Send a payload of user information to the ui
        """
        print("ChatConsumer: send_user_info_payload. ")
        await self.send_json({
            'user_info': user_info
            })


    async def display_progress_bar(self, is_displayed):
        """
        1. is_displayed = True
            - Display the progress bar on UI
        2. is_displayed = False
            - Hide the progress bar on UI
        """
        print("DISPLAY PROGRESS BAR: " + str(is_displayed))




    async def handle_client_error(self, e):
        """
        Called when a ClientError is raised.
        Sends error data to UI.
        """
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
            await self.send_json(errorData)
        return


@database_sync_to_async
def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    try:
        room = DirectMessageRoom.objects.get(pk=room_id)
    except DirectMessageRoom.DoesNotExist:
        raise ClientError("ROOM_INVALID", "Invalid room.")

    # Is this user allowed in the room? (must be user1 or user2)
    if user != room.user1 and user != room.user2:
        raise ClientError("ROOM_ACCESS_DENIED", "You do not have permission to join this room.")
    return room

@sync_to_async
def get_user_info(room, user):
    """
    Retrieve the user info for the user you are chatting with
    """
    try:
        # Determine who is who
        other_user = room.user1
        if other_user == user:
            other_user = room.user2

        payload = {}
        s = LazyAccountEncoder()
        # convert to list for serializer and select first entry (there will be only 1)
        payload['user_info'] = s.serialize([other_user])[0] 
        return json.dumps(payload)
    except ClientError as e:
        raise ClientError("DATA_ERROR", "Unable to get that users information.")
    return None   


@database_sync_to_async
def create_room_chat_message(room, user, message):
    return Message.objects.create(user=user, room=room, content=message)




