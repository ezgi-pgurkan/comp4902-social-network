from directmessage.models import DirectMessageRoom


def find_or_create_direct_message(user1, user2):
	try:
		directmessage = DirectMessageRoom.objects.get(user1=user1, user2=user2)
	except DirectMessageRoom.DoesNotExist:
		try:
			directmessage = DirectMessageRoom.objects.get(user1=user2, user2=user1)
		except DirectMessageRoom.DoesNotExist:
			directmessage = DirectMessageRoom(user1=user1, user2=user2)
			directmessage.save()
	return directmessage