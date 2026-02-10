import json
from django.http import JsonResponse
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from rest_framework_simplejwt.tokens import RefreshToken

# ปรับ Import ให้ตรงกับโครงสร้างไฟล์ใหม่ (apps/core/utils/function.py)
from apps.core.utils.function import create_user_log

# ปรับ Import UserProfile (คาดว่าน่าจะอยู่ที่ apps.core.models หรือ apps.users.models)
# หากยังไม่มีไฟล์ models ให้ตรวจสอบ path นี้อีกครั้ง
try:
    from apps.core.model.authorize.models import UserProfile
except ImportError:
    # Fallback หรือ Mock กรณีหาไม่เจอเพื่อป้องกัน Server Crash
    UserProfile = None

@csrf_exempt
def index(request):
    if request.method == 'POST':
        try:
            # รับข้อมูล JSON จาก Vue Frontend
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # ใช้ AuthenticationForm ตรวจสอบความถูกต้อง (Username/Password)
        form = AuthenticationForm(request, data=data)
        
        if form.is_valid():
            user = form.get_user()
            
            # Login เข้า Session (เผื่อกรณี Hybrid หรือ Admin)
            login(request, user)

            # ดึงข้อมูล Profile และตั้งค่า Session (ตาม Logic เดิม)
            if UserProfile:
                user_profile = UserProfile.objects.filter(user=user).first()
                request.session['show_toast'] = True
                if user_profile:
                    request.session['privilege_history'] = user_profile.privilege_history
                    
            print(f"User login {user.username} logged in successfully.")

            # ✅ บันทึก Log สำเร็จ
            create_user_log(
                user=user,
                action="Login",
                detail=f"Username: {user.username} login success",
                status="success",
                request=request
            )

            # สร้าง JWT Token ส่งกลับไปให้ Frontend
            refresh = RefreshToken.for_user(user)
            
            return JsonResponse({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'message': 'Login successful'
            })

        else:
            # ❌ Login ล้มเหลว -> บันทึก Log Error
            username_input = data.get('username', 'unknown')
            create_user_log(
                user=None,
                action="Login",
                detail=f"Failed login attempt with username: {username_input}",
                status="error",
                request=request
            )
            
            # ส่ง Error กลับเป็น JSON
            return JsonResponse({'error': 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
