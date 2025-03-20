from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Formulario para registrar usuarios
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    is_superuser = forms.BooleanField(required=False, label="¿Es administrador?")  # Nuevo campo

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser']

# Formulario para editar usuarios
class UserEditForm(UserChangeForm):
    password = None  # Oculta el campo de contraseña en la edición
    is_superuser = forms.BooleanField(required=False, label="¿Es administrador?")  # Nuevo campo

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser']
