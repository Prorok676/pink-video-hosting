from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_list, name='home'),
    path('upload/', views.upload_video, name='upload'),
path('like/<int:video_id>/', views.like_video, name='like_video'),
path('comment/<int:video_id>/', views.add_comment, name='add_comment'),
    path('admin-panel/', views.admin_video_list, name='admin_video_list'),
    path('admin-panel/toggle/<int:video_id>/', views.toggle_block_video, name='toggle_block'),
]