from django.contrib import admin
from django.urls import path
from plans import views as plans_views
from authentication import views as authentication_views

urlpatterns = [
    path('todos/', plans_views.todo_view, name='todo-index'),
    path('login/', authentication_views.login_for_session, name='login-for-session'),
    path('get-user/', authentication_views.get_user, name='get-user'),
    path('admin/', admin.site.urls)
]
