from directmessage.models import DirectMessageRoom

from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils import timezone
from datetime import datetime



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


def calculate_timestamp(timestamp):
	"""
	1. Today or yesterday:
		- EX: 'today at 10:56 AM'
		- EX: 'yesterday at 5:19 PM'
	2. other:
		- EX: 05/06/2020
		- EX: 12/28/2020
	"""
	ts = ""
	# Today or yesterday
	if (naturalday(timestamp) == "today") or (naturalday(timestamp) == "yesterday"):
		str_time = datetime.strftime(timestamp, "%I:%M %p")
		str_time = str_time.strip("0")
		ts = f"{naturalday(timestamp)} at {str_time}"
	# other days
	else:
		str_time = datetime.strftime(timestamp, "%m/%d/%Y")
		ts = f"{str_time}"
	return str(ts)
