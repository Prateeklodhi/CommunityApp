from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('',views.home,name="home"),
    path('room<int:roomid>/',views.room,name="room"),
    path('create-room/',views.createRoom,name='createroom'),
    path('update-room/<str:pk>',views.updateRoom,name="updateroom"),
    path('delete_room/<str:pk>',views.deleteRoom,name="deleteroom"),
    path('delete_message/<str:pk>',views.deleteMessage,name="deletemessage"),
    path("profile/<str:pk>",views.userprofile,name = 'profile'),
]       