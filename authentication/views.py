from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from domain.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class SignupView(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        nickname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=nickname).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=nickname, email=email, password=password)
        login(request, user)
        return redirect('dashboard')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'dashboard.html')