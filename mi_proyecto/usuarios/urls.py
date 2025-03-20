from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 🔹 Rutas para gestión de usuarios
    path('usuarios/', views.manage_users, name='manage_users'),
    path('usuarios/registrar/', views.register_user, name='register_user'),
    path('usuarios/editar/<int:user_id>/', views.edit_user, name='edit_user'),
    path('usuarios/eliminar/<int:user_id>/', views.delete_user, name='delete_user'),
]
