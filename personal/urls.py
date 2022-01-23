from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from personal import views


app_name = 'personal'

urlpatterns = [
    path('post/<int:pk>', views.postDetailView, name='postdetail'),
    path('add_post/', views.addPostView, name='add-post'),


] 

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)