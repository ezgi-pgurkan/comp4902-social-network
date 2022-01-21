from django.shortcuts import render, redirect
from django.conf import settings
from itertools import chain
import json
from django.http import HttpResponse

from directmessage.models import DirectMessageRoom, Message
from directmessage.utils import find_or_create_direct_message
from account.models import Account

DEBUG = False

def direct_message_room_view(request, *args, **kwargs):
	user = request.user

	# Redirect if not authenticated
	if not user.is_authenticated:
		return redirect("login")

	context = {}

	# Finds all the rooms the user is a part of
	rooms1=DirectMessageRoom.objects.filter(user1=user, is_active=True)
	rooms2=DirectMessageRoom.objects.filter(user2=user, is_active=True)

	# Merge the lists, will remove duplicate entries
	rooms= list(chain(rooms1, rooms2))

	# messages and recipients m_and_r
	m_and_r = []
	for room in rooms:
		if room.user1 == user:
			recipient = room.user2
		else:
			recipient = room.user1
		m_and_r.append({
			"message": "",
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
				directmessage = find_or_create_direct_message(user1, user2)
				payload['response'] = "Successfully got the chat."
				payload['chatroom_id'] = directmessage.id#!!!!!!!!!!!!!!!!!!!!
			except Account.DoesNotExist:
				payload['response'] = "Unable to start a chat with that user."
	else:
		payload['response'] = "You can't start a chat if you are not authenticated."
	return HttpResponse(json.dumps(payload), content_type="application/json")

