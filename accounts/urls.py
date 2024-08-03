from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.tests, name='tests'),
    # path('chat/', views.twilio, name='chat'),
    path('send_token', views.send_token, name='send_token'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('register/', views.register, name='register'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
]
