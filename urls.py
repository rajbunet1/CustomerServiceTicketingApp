from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_tickets, name='home_tickets'),

    path("register", views.signup_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),

    path('home_tickets', views.home_tickets, name='home_tickets'),
    path('new_ticket', views.create_ticket, name='new_ticket'),
    path('edit_ticket/<int:id>', views.update_ticket, name='edit_ticket'),
    path('delete_ticket/<int:id>', views.delete_ticket, name='delete_ticket'),
    path('respond_ticket/<int:id>', views.respond_ticket, name='respond_ticket'),

    path('home_users', views.home_users, name='home_users'),
    path('new_user', views.create_user, name='new_user'),
    path('edit_user/<int:id>', views.update_user, name='edit_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),

    path('download_ticket_files/<int:id>', views.download_ticket_files, name='download_ticket_files'),
]
