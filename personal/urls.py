from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from personal import views


app_name = 'personal'

urlpatterns = [
    path('add_post/', views.addPostView, name='add-post'),
    path('delete_post/<str:pk>', views.deletePostView, name='delete-post'),
    path('edit_post/<str:pk>', views.editPostView, name='edit-post'),
    path('liked/', views.like_unlike_post, name='like-post-view'),
    path('save-comment/', views.save_comment, name='save-comment'),
] 

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

