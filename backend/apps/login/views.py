import socket
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm

from core.utils.function import create_user_log,get_user_os_browser_architecture

@never_cache
def index(request):
    server_ip = socket.gethostbyname(socket.gethostname())
    info = get_user_os_browser_architecture(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            user_profile = UserProfile.objects.filter(user=user).first()
            request.session['show_toast'] = True

            if user_profile:
                request.session['privilege_history'] = user_profile.privilege_history

            create_user_log(user=user,action="Login",detail=f"Username: {user.username} login success",status="success",request=request)

            return redirect('/home')

        else:
            # ❌ login ล้มเหลว -> บันทึก log error
            username_input = request.POST.get('username', '(unknown)')
            messages.error(request, 'รหัสผ่านไม่ถูกต้อง')
            create_user_log(user=None,action="Login",detail=f"Failed login attempt with username: {username_input}",status="error",request=request)
            

    else:
        form = AuthenticationForm()

    return render(request, 'login/index.html', {'form': form})

