from django.shortcuts import render, redirect
from django.conf import settings
from itertools import chain
import json
import datetime
from datetime import datetime as dt
import pytz
from django.http import HttpResponse

from directmessage.models import DirectMessageRoom, Message
from directmessage.utils import find_or_create_direct_message
from account.models import Account

DEBUG = False

def direct_message_room_view(request, *args, **kwargs):
	user = request.user
	room_id=request.GET.get("room_id")

	# Redirect if not authenticated
	if not user.is_authenticated:
		return redirect("login")

	context = {}
	if room_id:
		try:
			room = DirectMessageRoom.objects.get(pk=room_id)
			context['room'] = room
		except DirectMessageRoom.DoesNotExist:
			pass

	# Finds all the rooms the user is a part of
	# we dont know if user is user1 or user2
	rooms1=DirectMessageRoom.objects.filter(user1=user, is_active=True)
	rooms2=DirectMessageRoom.objects.filter(user2=user, is_active=True)

	# Merge the lists, will remove duplicate entries
	# chain -> merge 
	rooms= list(chain(rooms1, rooms2))

	# messages and recipients m_and_r
	# [{"message": "hey", "recipient": "Jake"}, {"message": "hello", "recipient": "Blake"},]
	m_and_r = []
	for room in rooms:
		# find who is the recipient
		if room.user1 == user:
			recipient = room.user2
		else:
			recipient = room.user1

		# find the last message the recipient sent
		try:
			message = Message.objects.filter(room=room, user=recipient).latest("timestamp")
		except Message.DoesNotExist:
			# create a dummy message with dummy timestamp if the message does not exist
			today = dt(
				year=1950, 
				month=1, 
				day=1, 
				hour=1,
				minute=1,
				second=1,
				tzinfo=pytz.UTC
			)
			message = Message(
				user=recipient,
				room=room,
				timestamp=today,
				content="",
			)

		m_and_r.append({
			"message": message,
			"recipient": recipient
			})

		context['m_and_r'] = m_and_r


	context['debug'] = DEBUG
	context['debug_mode'] = settings.DEBUG
	return render(request, "directmessage/room.html", context)


# Ajax call to return a private chatroom or create one if does not exist
def create_or_return_private_chat(request, *args, **kwargs):
	user1 = request.user
	payload = {}
	if user1.is_authenticated:
		if request.method == "POST":
			user2_id = request.POST.get("user2_id")
			try:
				user2 = Account.objects.get(pk=user2_id)
				directmessage = find_or_create_direct_message(user1, user2)#chatroom
				payload['response'] = "Successfully got the chat."
				payload['chatroom_id'] = directmessage.id
			except Account.DoesNotExist:
				payload['response'] = "Unable to start a chat with that user."
	else:
		payload['response'] = "You can't start a chat if you are not authenticated."
	return HttpResponse(json.dumps(payload), content_type="application/json")

