from django.urls import path

from Base.views import home, createRoom, updateRoom, deleteRoom, room, deleteMessage, topics, activity, profile, registerUser, updateUser, loginUser, logoutUser

urlpatterns = [
    path('', home, name='Home'),
    path('profile/<int:id>', profile, name='Profile'),
    path('topics/', topics, name='Topics'),
    path('activity/', activity, name='Activity'),
    path('room/<int:id>', room, name='Room'),
    path('room/create/', createRoom, name='create_room'),
    path('room/edit/<int:id>', updateRoom, name='update_room'),
    path('room/delete/<int:id>', deleteRoom, name='delete_room'),
    path('message/delete/<int:id>', deleteMessage, name='delete_message'),
    path('auth/user/register', registerUser, name='register_user'),
    path('auth/user/edit/', updateUser, name='edit_user'),
    path('auth/login/', loginUser, name='Login'),
    path('auth/logout/', logoutUser, name='Logout'),
]
