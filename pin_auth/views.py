from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import User
from .forms import RegisterForm, LoginForm

class RegisterView(View):
    def get(self, request):
        if 'user_id' in request.session:
            return redirect('home')
            
        form = RegisterForm()
        return render(request, 'pin_auth/register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pin = form.cleaned_data['pin']
            user.set_pin(pin)
            user.save()
            messages.success(request, f"Registration successful for {user.name}!")
            return redirect('login')
        return render(request, 'pin_auth/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if 'user_id' in request.session:
            return redirect('home')
            
        form = LoginForm()
        keypad_numbers = list(range(10))
        random.shuffle(keypad_numbers)
        return render(request, 'pin_auth/login.html', {
            'form': form,
            'keypad_numbers': json.dumps(keypad_numbers)
        })
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            pin = form.cleaned_data['pin']
            entry_time = request.POST.get('entry_time', '0')
            attempts = request.POST.get('attempts', '0')
            
            try:
                entry_time = float(entry_time)
                attempts = int(attempts)
            except (ValueError, TypeError):
                entry_time = 0
                attempts = 0
            request.session['pin_attempts'] = attempts
            login_attempt = {
                'timestamp': timezone.now().isoformat(),
                'name': name,
                'entry_time': entry_time,
                'attempts': attempts,
                'status': 'pending',  
                'ip': request.META.get('REMOTE_ADDR', ''),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')
            }
            
            try:
                user = User.objects.get(name=name)
                if user.check_pin(pin):
                    login_attempt['status'] = 'success'
                    request.session['user_id'] = user.id
                    request.session['last_login_time'] = entry_time
                    request.session['login_attempts'] = attempts
                    if 'pin_attempts' in request.session:
                        del request.session['pin_attempts']
                    self._update_login_history(request, login_attempt)
                    
                    messages.success(request, f"Welcome back, {user.name}!")
                    return redirect('home')
                else:
                    login_attempt['status'] = 'failed'
                    login_attempt['reason'] = 'invalid_pin'
                    self._update_login_history(request, login_attempt)
                    
                    messages.error(request, "Invalid PIN")
            except User.DoesNotExist:
                
                login_attempt['status'] = 'failed'
                login_attempt['reason'] = 'user_not_found'
                self._update_login_history(request, login_attempt)
                
                messages.error(request, "User not found")
        keypad_numbers = list(range(10))
        random.shuffle(keypad_numbers)
        return render(request, 'pin_auth/login.html', {
            'form': form,
            'keypad_numbers': json.dumps(keypad_numbers)
        })
    
    def _update_login_history(self, request, login_attempt):
        """Helper method to update login history in session"""
        login_history = request.session.get('login_history', [])
        login_history.append(login_attempt)
        if len(login_history) > 20:
            login_history = login_history[-20:]
        
        request.session['login_history'] = login_history


class HomeView(View):
    def get(self, request):
        if 'user_id' not in request.session:
            messages.error(request, "Please login first")
            return redirect('login')
        try:
            user = User.objects.get(id=request.session['user_id'])
            return render(request, 'pin_auth/home.html', {'user': user})
        except User.DoesNotExist:
            del request.session['user_id']
            messages.error(request, "User not found")
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        if 'user_id' in request.session:
            del request.session['user_id']
        messages.success(request, "You have been logged out successfully!")
        return redirect('login')
    
class ShoulderSurfingProtectionView(View):
    @csrf_exempt
    def post(self, request):
        if not request.is_ajax():
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)     
        try:
            data = json.loads(request.body)
            settings = {
                'enableCombinedProtection': data.get('enableCombinedProtection', False)
            }
            request.session['protection_settings'] = settings
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    def get(self, request):
        settings = request.session.get('protection_settings', {
            'enableCombinedProtection':False
        })
        
        return JsonResponse(settings)
    def detect_suspicious_login_attempts(request, user):
        ip_address = request.META.get('REMOTE_ADDR', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        login_history = request.session.get('login_history', [])
        risk_level = 0
        current_time = timezone.now()
        recent_attempts = [
            login for login in login_history 
            if (current_time - login['timestamp']).seconds < 3600  
        ]
    
        if len(recent_attempts) > 5:
            risk_level += 1
        recent_ips = set(login['ip'] for login in recent_attempts)
        if len(recent_ips) > 2:
            risk_level += 2
        hour = current_time.hour
        if hour < 5 or hour > 23:  
            risk_level += 1
        login_history.append({
            'timestamp': current_time,
            'ip': ip_address,
            'user_agent': user_agent
     })
        if len(login_history) > 20:
            login_history = login_history[-20:]
        
        request.session['login_history'] = login_history
    
        return risk_level
