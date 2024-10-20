from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login_page",views.login_page,name="login_page"),
    path("register",views.register,name="register"),
    path("feedback",views.feedback,name="feedback"),
    path('experiments',views.experiment,name="experiments"),
    path("about",views.about,name="about"),
    path("help",views.help,name="help")
]