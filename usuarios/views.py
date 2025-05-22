from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CadastroForm, LoginForm

def login_view(request):
    next_url = request.GET.get('next', '') or request.POST.get('next', '') or 'home'
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  # AuthenticationForm precisa do request como primeiro argumento
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('home')

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CadastroForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})
