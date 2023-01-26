from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='home'),

    path('login/', auth_views.LoginView.as_view(template_name='quora/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='quora/logout.html'), name='logout'),

    path("register/", views.user_register, name="register"),

    path("create_question", views.create_question, name='create_question'),
    path("question_detail/<int:id>", views.question_detail, name='question_detail'),
    path("upvote/<int:id>/", views.vote_up, name="upvote"),
    path("downvote/<int:id>/", views.vote_down, name="downvote"),
    path("accept_as_answer/<int:id>/",
         views.accept_as_answer, name="accept_as_answer"),
    path("unaccept_as_answer/<int:id>/",
         views.unaccept_as_answer, name="unaccept_as_answer"),

    path("view_profile/<int:id>/", views.view_profile, name="view_profile"),
]
