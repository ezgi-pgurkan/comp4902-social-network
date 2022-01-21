from django.urls import path

from directmessage.views import(
	direct_message_room_view,
	create_or_return_private_chat,
)

app_name = 'directmessage'

urlpatterns = [
	path('', direct_message_room_view, name='direct-message-room'),
	path('create_or_return_private_chat/', create_or_return_private_chat, name='create-or-return-private-chat'),

]




