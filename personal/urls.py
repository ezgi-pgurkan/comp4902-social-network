from django.urls import path, include

from personal import views

app_name = 'personal'

urlpatterns = [
    path('post/<int:pk>', views.postDetailView, name='postdetail'),


] 

