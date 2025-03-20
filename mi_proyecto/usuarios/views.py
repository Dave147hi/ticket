from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserEditForm

# 🔹 Verifica si el usuario es administrador
def is_admin(user):
    return user.is_superuser

# 🔹 Vista para listar usuarios (Solo admin)
@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'usuarios/manage_users.html', {'users': users})

# 🔹 Vista para registrar un nuevo usuario (Solo admin)
@login_required
@user_passes_test(is_admin)
def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('manage_users')
    else:
        form = UserRegisterForm()
    return render(request, 'usuarios/register_user.html', {'form': form})

# 🔹 Vista para editar un usuario (Solo admin)
@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('manage_users')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'usuarios/edit_user.html', {'form': form, 'user': user})

# 🔹 Vista para eliminar un usuario (Solo admin)
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('manage_users')
    return render(request, 'usuarios/delete_user.html', {'user': user})

# 🔹 Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

# 🔹 Dashboard
@login_required
def dashboard_view(request):
    return render(request, 'usuarios/dashboard.html', {'user': request.user})

# 🔹 Logout
def logout_view(request):
    logout(request)
    return redirect('login')
