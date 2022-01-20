from django.shortcuts import render, redirect
from django.conf import settings
from itertools import chain

from directmessage.models import DirectMessageRoom, Message

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