from django.urls import path

from directmessage.views import(
	direct_message_room_view,
)

app_name = 'directmessage'

urlpatterns = [
	path('', direct_message_room_view, name='direct-message-room'),
]