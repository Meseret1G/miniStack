from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
    path('logout/',views.logoutPage,name='logout'),
    path('',views.home, name='home'),
    path('post/<str:pk>/',views.post, name='post'),
    path('form/',views.createPost, name='createpost'),
    path('update/<str:pk>/',views.updatePost, name='editpost'),
    path('delete/<str:pk>/',views.deletePost, name='deletepost'),
    path('deletecomment/<str:pk>/',views.deleteComment, name='deletecomment'),
    path('profile/<str:pk>/',views.userProfile,name='userprofile'),
    path('edituser/',views.editUser, name='edituser'),
]