from django.urls import path

from account.views import (
	account_view,
	edit_account_view,
	profile_view,
	editProfileView,
)

app_name = 'account'

urlpatterns = [
	path('<user_id>/', account_view, name="view"),
	path('<user_id>/edit/', edit_account_view, name="edit"),
	path('<user_id>/profile_page/', profile_view, name="profile-page"),
    path('<user_id>/edit_profile/', editProfileView, name='edit-profile' ),

]