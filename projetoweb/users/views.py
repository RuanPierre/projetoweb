from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegistroForm

def cadastro(request):
    if request.method == 'GET':
        form = RegistroForm()
        return render(request, 'users/cadastro.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegistroForm(request.POST) 
       
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request,f'Olá {user.username.title()}, você foi cadastrado')
            return redirect('home')
        else:
            messages.error(request,f'Cadastro inválido, tente novamente.')
            return render(request, 'users/cadastro.html', {'form': form})

def entrar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Olá {username.title()}, bem-vindo de volta')
                return redirect('home')
            
        
        messages.error(request,f'Nome ou senha invalidos')
        return render(request,'users/login.html',{'form': form})
        
def sair(request):
    logout(request)
    messages.success(request,f'Você saiu.')
    return redirect('login')   