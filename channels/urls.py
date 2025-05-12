from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('channels/', views.channels_list, name='channels_list'),
    path('delete/<int:channel_id>/', views.delete_channel, name='delete_channel'),
    path('tasks/', views.tasks, name='tasks'),
    path('files/', views.files, name='files'),
    path('check-status/', views.check_stream_status, name='check_stream_status'),
]
