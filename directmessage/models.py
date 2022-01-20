from django.db import models
from django.conf import settings

class DirectMessageRoom(models.Model):

	#A private communication channel between two users.

	user1 =	models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user1")
	user2 =	models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user2")
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return f"A chat between {user1} and {user2}."

	@property
	def group_name(self):
		return f"DirectMessageRoom-{self.id}"


class MessageManager(models.Manager):
	def by_room(self, room):
		qs = Message.objects.filter(room=room).order_by("-timestamp")
		return qs


class Message(models.Model):

	# A chat message created by a user inside a room.

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	room = models.ForeignKey(DirectMessageRoom, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	content = models.TextField(unique=False, blank=False)

	objects = MessageManager()

	def __str__(self):
		return self.content
