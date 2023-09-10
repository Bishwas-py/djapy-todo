from django.contrib import admin
from django.urls import path
from plans import views as plans_views

urlpatterns = [
    path('', plans_views.todo_view, name='todo-index'),
    path('login/', plans_views.login_for_session, name='login-for-session'),
    path('admin/', admin.site.urls)
]
