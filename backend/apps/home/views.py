from django.shortcuts import render, redirect
from functools import wraps
from django.contrib.auth.decorators import login_required
# from utils.function import BaseListAPIView,PageNumberPagination
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import os
import subprocess
from datetime import datetime
import base64
import socket
from datetime import datetime, timedelta
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from apps.core.utils.function import create_user_log, get_user_os_browser_architecture

# models
from apps.core.model.authorize.models import UserAuth,MainDatabase,SetAudio,UserLog,UserProfile,Agent
from apps.core.model.audio.models import AudioInfo
from .models import FavoriteSearch, ViewAudio,tbSetColumn, PlaybackLog,ConfigKey
from .serializers import FavoriteSearchSerializer

#serializer
from apps.core.model.authorize.serializers import MainDatabaseSerializer

one_year_ago = timezone.now() - timedelta(days=365)

server_ip = socket.gethostbyname(socket.gethostname())

def check_permission(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_auth = UserAuth.objects.filter(user=user).first()
            if user_auth and not user_auth.status:
                return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required(login_url='/login')
def ApiIndexHome(request):
    show_toast = request.session.get('show_toast', False)
    if show_toast:
        del request.session['show_toast']

    set_audio = SetAudio.objects.filter(user=request.user).first()
    user_auth_qs = UserAuth.objects.filter(user=request.user, allow=True)
    # get MainDatabase objects allowed for this user
    main_db_ids = list(user_auth_qs.values_list('maindatabase_id', flat=True))
    main_db = MainDatabase.objects.filter(id__in=main_db_ids).order_by('database_name')
    user_profile = UserProfile.objects.filter(user=request.user).first()
    favorite_search = FavoriteSearch.objects.filter(user=request.user).first()
    favorite_search_all = FavoriteSearch.objects.filter(user=request.user).all()
    audio_column = tbSetColumn.objects.filter(user=request.user).first()
    agent = Agent.objects.all()
    raw_data = favorite_search.raw_data if favorite_search else {}

    main_db_serialized = MainDatabaseSerializer(main_db, many=True).data
    favorite_search_all_serialized = FavoriteSearchSerializer(favorite_search_all, many=True).data
    favorite_search_serialized = FavoriteSearchSerializer(favorite_search).data if favorite_search else None

    return JsonResponse({
        'show_toast': show_toast,
        'main_db': main_db_serialized,
        'set_audio': set_audio.audio_path if set_audio else None,
        'user_profile': {'id': user_profile.user.id, 'username': user_profile.user.username} if user_profile else None,
        'favorite_search': favorite_search_serialized,
        'raw_data': raw_data,
        'favorite_search_all': favorite_search_all_serialized,
        'audio_column': audio_column.raw_data if audio_column else 0,
        'agent': list(agent.values('id', 'agent_code', 'first_name', 'last_name')),
    })
    
@login_required(login_url='/login')
def ApiGetAudioList(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 25))
    # sanitize pagination params
    try:
        start = max(0, int(start))
    except Exception:
        start = 0
    try:
        length = max(1, min(1000, int(length)))
    except Exception:
        length = 25

    search_value = (request.GET.get("search[value]", "") or "").strip()

    set_audio = SetAudio.objects.filter(user=request.user).first()
    main_db_id = UserAuth.objects.filter(user=request.user, allow=True).values_list("maindatabase_id", flat=True)

    audio_list = AudioInfo.objects.select_related("audiofile", "agent", "customer") \
        .filter(main_db__in=main_db_id)
    
    # audio_list = ViewAudio.objects.all()

    # ฟิลเตอร์จาก request.form หรือ request.GET
    database_name = request.POST.get("database_name") or request.GET.get("database_name")  
    start_date = request.POST.get("start_date") or request.GET.get("start_date") 
    end_date = request.POST.get("end_date") or request.GET.get("end_date")
    file_name = request.POST.get("file_name") or request.GET.get("file_name")
    duration = request.POST.get("duration") or request.GET.get("duration")
    customer = request.POST.get("customer") or request.GET.get("customer") 
    agent_id = request.POST.get("agent_id") or request.GET.get("agent_id")
    agent_group = request.POST.get("agent_group") or request.GET.get("agent_group")
    time_type = request.POST.get("type") or request.GET.get("type")
    
    call_direction = request.POST.get("call_direction") or request.GET.get("call_direction")
    extension = request.POST.get("extension") or request.GET.get("extension")
    agent_name = request.POST.get("agent") or request.GET.get("agent")
    full_name = request.POST.get("full_name") or request.GET.get("full_name")
    
    now = datetime.now()
    if time_type:
        if time_type == "hour":
            start_date = now - timedelta(hours=1)
        elif time_type == "day":
            start_date = now - timedelta(days=1)
        elif time_type == "month":
            start_date = now - timedelta(days=30)
        elif time_type == "year":
            start_date = now - timedelta(days=365)
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date = now.strftime("%Y-%m-%d %H:%M:%S")
        

    if database_name and database_name != "all":
        parts = [p.strip() for p in str(database_name).split(',') if p.strip()]
        if parts:
            ids = []
            names = []
            for p in parts:
                try:
                    ids.append(int(p))
                except Exception:
                    names.append(p)
            if ids:
                audio_list = audio_list.filter(main_db__id__in=ids)
            elif names:
                qn = Q()
                for n in names:
                    qn |= Q(main_db__database_name__icontains=n)
                audio_list = audio_list.filter(qn)

    if search_value:
        parts = search_value.split(",")
        q_global = None
        for part in parts:
            part = part.strip()
            if part:
                q_search = (
                    Q(call_direction__icontains=part) |
                    Q(extension__icontains=part) |
                    Q(agent__first_name__icontains=part) |
                    Q(agent__last_name__icontains=part) |
                    Q(customer_number__icontains=part) |
                    Q(agent__agent_code__icontains=part)
                )
                name_parts = part.split(" ", 1)
                if len(name_parts) == 2:
                    first, last = name_parts
                    q_search |= (Q(agent__first_name__icontains=first) & Q(agent__last_name__icontains=last))
                
                if q_global is None:
                    q_global = q_search
                else:
                    q_global &= q_search
        
        if q_global:
            audio_list = audio_list.filter(q_global)
            
    # Mapping simple filters
    filter_map = {
        "start_datetime__gte": start_date,
        "end_datetime__lte": end_date,
        "audiofile__file_name__icontains": file_name,
        "duration_seconds__icontains": duration,
    }

    for field, value in filter_map.items():
        if value:
            audio_list = audio_list.filter(**{field: value})

    if customer:
        parts = [p.strip() for p in customer.split(',') if p.strip()]
        if parts:
            q = Q()
            for p in parts:
                q |= Q(customer_number__icontains=p)
            audio_list = audio_list.filter(q)

    if extension:
        parts = [p.strip() for p in extension.split(',') if p.strip()]
        if parts:
            q = Q()
            for p in parts:
                q |= Q(extension__icontains=p)
            audio_list = audio_list.filter(q)

    if agent_id:
        parts = [p.strip() for p in str(agent_id).split(',') if p.strip()]
        if parts:
            ids = []
            codes = []
            for p in parts:
                try:
                    ids.append(int(p))
                except Exception:
                    codes.append(p)
            if ids:
                audio_list = audio_list.filter(agent__id__in=ids)
            if codes:
                q = Q()
                for c in codes:
                    q |= Q(agent__agent_code__icontains=c)
                audio_list = audio_list.filter(q)

    if agent_group:
        groups = [g.strip() for g in agent_group.split(',') if g.strip()]
        if groups:
            audio_list = audio_list.filter(agent__agent_group_id__in=groups)

    if call_direction and call_direction != "all":
        parts = [p.strip() for p in call_direction.split(',') if p.strip()]
        if parts:
            q = Q()
            for p in parts:
                q |= Q(call_direction__icontains=p)
            audio_list = audio_list.filter(q)

    if agent_name:
        parts = agent_name.split(',')
        q_agent = Q()
        for part in parts:
            part = part.strip()
            if not part: continue
            
            if " - " in part:
                code_part, name_part = part.split(" - ", 1)
                code_part = code_part.strip()
                name_part = name_part.strip()
                
                q_sub = Q(agent__agent_code__icontains=code_part)
                if name_part:
                    name_parts = name_part.split(" ", 1)
                    if len(name_parts) == 2:
                        first, last = name_parts
                        q_sub &= (Q(agent__first_name__icontains=first) & Q(agent__last_name__icontains=last))
                    else:
                        q_sub &= (Q(agent__first_name__icontains=name_part) | Q(agent__last_name__icontains=name_part))
                q_agent |= q_sub
            else:
                name_parts = part.split(" ", 1)
                if len(name_parts) == 2:
                    first, last = name_parts
                    q_agent |= ((Q(agent__first_name__icontains=first) & Q(agent__last_name__icontains=last)) | Q(agent__agent_code__icontains=part))
                else:
                    q_agent |= (Q(agent__first_name__icontains=part) | Q(agent__last_name__icontains=part) | Q(agent__agent_code__icontains=part))
        if q_agent:
            audio_list = audio_list.filter(q_agent)

    if full_name:
        parts = full_name.split(',')
        q_full = Q()
        for part in parts:
            part = part.strip()
            if not part: continue
            name_parts = part.split(" ", 1)
            if len(name_parts) == 2:
                first, last = name_parts
                q_full |= (Q(agent__first_name__icontains=first) & Q(agent__last_name__icontains=last))
            else:
                q_full |= (Q(agent__first_name__icontains=part) | Q(agent__last_name__icontains=part))
        if q_full:
            audio_list = audio_list.filter(q_full)



    # count after applying filters
    records_total = audio_list.count()

    # Pagination (slice)
    audio_page = audio_list[start:start + length]

    data = []
    for idx, audio in enumerate(audio_page, start=start+1):
        main_db_display = str(audio.main_db) if hasattr(audio, 'main_db') else ''
        start_dt = audio.start_datetime.strftime("%Y-%m-%d %H:%M") if getattr(audio, 'start_datetime', None) else "-"
        end_dt = audio.end_datetime.strftime("%Y-%m-%d %H:%M") if getattr(audio, 'end_datetime', None) else "-"
        file_name = audio.audiofile.file_name if getattr(audio, 'audiofile', None) else "-"
        duration_val = str(audio.audiofile.duration) if (getattr(audio, 'audiofile', None) and getattr(audio.audiofile, 'duration', None)) else "-"
        agent_display = str(audio.agent) if getattr(audio, 'agent', None) else "-"
        full_name = f"{audio.agent.first_name} {audio.agent.last_name}" if getattr(audio, 'agent', None) else "-"

        data.append({
            "no": idx,
            "main_db": main_db_display,
            "start_datetime": start_dt,
            "end_datetime": end_dt,
            "file_name": file_name,
            "duration": duration_val,
            "call_direction": audio.call_direction,
            "customer_number": audio.customer_number,
            "extension": audio.extension,
            "agent": agent_display,
            "full_name": full_name,
            "file_path": audio.audiofile.file_path if getattr(audio, 'audiofile', None) else None,
            "set_audio": set_audio.audio_path if set_audio else None,
            "custom_field_1": ""
        })
        


    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_total,
        "data": data
    })

def ApiSaveMyFavoriteSearch(request):
    if request.method == "POST":
        action = request.POST.get("action")
        user = request.user
        
        # Handle Delete
        if action == "delete":
            favorite_id = request.POST.get("favorite_id")
            try:
                fav = FavoriteSearch.objects.get(id=favorite_id, user=user)
                fav_name = fav.favorite_name
                fav.delete()
                create_user_log(user=request.user, action="Delete Favorite", detail=f"Deleted favorite: {fav_name}", status="success", request=request)
                return JsonResponse({"status": "success", "message": "Deleted successfully", "id": favorite_id})
            except Exception as e:
                create_user_log(user=request.user, action="Delete Favorite", detail=f"Error deleting favorite: {str(e)}", status="error", request=request)
                return JsonResponse({"status": "error", "message": str(e)})

        # Handle Create and Edit
        favorite_name = request.POST.get("favorite_name", "").strip()
        description = request.POST.get("favorite_description") or request.POST.get("create_favorite_description", "")
        full_name = request.POST.get("full_name") or request.POST.get("fav_fullname", "")

        
        # Collect raw data from form fields
        raw_data = {
            "database_name": request.POST.get("database_name", ""),
            "call_direction": request.POST.get("call_direction", ""),
            "start_date": request.POST.get("start_date", ""),
            "end_date": request.POST.get("end_date", ""),
            "file_name": request.POST.get("file_name", ""),
            "customer": request.POST.get("customer", ""),
            "extension": request.POST.get("extension", ""),
            "agent": request.POST.get("agent", ""),
            "full_name": full_name,
        }

        if action == "create":
            if FavoriteSearch.objects.filter(user=user, favorite_name__iexact=favorite_name).exists():
                create_user_log(user=request.user, action="Create Favorite", detail=f"Duplicate name: {favorite_name}", status="error", request=request)
                return JsonResponse({"status": "error", "message": "This name is already in the system."})

            try:
                fav = FavoriteSearch.objects.create(
                    user=user,
                    favorite_name=favorite_name,
                    raw_data=raw_data,
                    description=description
                )
                create_user_log(user=request.user, action="Create Favorite", detail=f"Created favorite: {favorite_name}", status="success", request=request)
                return JsonResponse({
                    "status": "success", 
                    "message": "Created successfully",
                    "favorite": {
                        "id": fav.id,
                        "favorite_name": fav.favorite_name,
                        "raw_data": fav.raw_data,
                        "description": fav.description
                    }
                })
            except Exception as e:
                create_user_log(user=request.user, action="Create Favorite", detail=f"Error creating favorite: {str(e)}", status="error", request=request)
                return JsonResponse({"status": "error", "message": str(e)})

        elif action == "edit":
            favorite_id = request.POST.get("favorite_id")
            
            if FavoriteSearch.objects.filter(user=user, favorite_name__iexact=favorite_name).exclude(id=favorite_id).exists():
                create_user_log(user=request.user, action="Edit Favorite", detail=f"Duplicate name: {favorite_name}", status="error", request=request)
                return JsonResponse({"status": "error", "message": "This name is already in the system."})

            try:
                fav = FavoriteSearch.objects.get(id=favorite_id, user=user)
                fav.favorite_name = favorite_name
                fav.raw_data = raw_data
                fav.description = description
                fav.save()
                create_user_log(user=request.user, action="Edit Favorite", detail=f"Updated favorite: {favorite_name}", status="success", request=request)
                return JsonResponse({
                    "status": "success", 
                    "message": "Updated successfully",
                    "favorite": {
                        "id": fav.id,
                        "favorite_name": fav.favorite_name,
                        "raw_data": fav.raw_data,
                        "description": fav.description
                    }
                })
            except FavoriteSearch.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Favorite not found"})
            except Exception as e:
                create_user_log(user=request.user, action="Edit Favorite", detail=f"Error updating favorite: {str(e)}", status="error", request=request)
                return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def ApiCheckMyFavoriteName(request):
    favorite_name = request.GET.get('favoriteName', '').strip()
    favorite_id = request.GET.get('favoriteId', None)
    
    if not favorite_name:
        return JsonResponse({'status': 'success', 'is_taken': False})

    query = FavoriteSearch.objects.filter(user=request.user, favorite_name__iexact=favorite_name)
    if favorite_id:
        query = query.exclude(id=favorite_id)

    if query.exists():
        return JsonResponse({'status': 'success', 'is_taken': True, 'message': 'This name is already in the system.'})
    else:
        return JsonResponse({'status': 'success', 'is_taken': False})
    
# --- Encryption Helper (Simple XOR + Base64) ---
SECRET_KEY = b"9Xv2M4p7Q8r1Z3w5Y6t8B0n2V4c6X8m0L2k4J6h8F0d2S4a" # (ต้องตรงกับ Wrapper exe)

def encrypt_credential(text):
    if not text: return ""
    data = text.encode('utf-8')
    encrypted = bytes(a ^ b for a, b in zip(data, SECRET_KEY * (len(data) // len(SECRET_KEY) + 1)))
    return base64.b64encode(encrypted).decode('utf-8')
    
@login_required
def ApiGetCredentials(request):
    """
    API endpoint ที่ส่งข้อมูล username/password สำหรับเชื่อมต่อ network share
    โดยดึงข้อมูลจากโมเดล ConfigKey
    """
    try:
        # ดึงข้อมูลโดยใช้ 'type' เพื่อระบุว่าเป็น username หรือ password
        config_key = ConfigKey.objects.get(type='player_connect')
        info = get_user_os_browser_architecture(request)

        credentials = {
            "username": encrypt_credential(config_key.key_username),
            "password": encrypt_credential(config_key.key_password)
        }
        return JsonResponse(credentials)
    except ConfigKey.DoesNotExist:
        UserLog.objects.create(
            user=request.user,
            action="Credentials",
            detail={"error": "Credentials not configured. Please create 'niceplayer_username' and 'niceplayer_password' types in ConfigKey."},
            status="error",
            client_type=f"{info['os']} / {info['browser']}",
            ip_address=server_ip,  
        )
        return JsonResponse({"error": "Credentials not configured. Please create 'niceplayer_username' and 'niceplayer_password' types in ConfigKey."}, status=500)
    except Exception as e:
        UserLog.objects.create(
            user=request.user,
            action="Credentials",
            detail={"error": str(e)},
            status="error",
            client_type=f"{info['os']} / {info['browser']}",
            ip_address=server_ip,  
        )
        return JsonResponse({"error": str(e)}, status=500)
    
@require_POST
def ApiLogPlayAudio(request):
    """
    API endpoint สำหรับรับ Log การเล่นไฟล์เสียงจาก Frontend
    """
    try:
        info = get_user_os_browser_architecture(request)
        data = json.loads(request.body)

        UserLog.objects.create(
            user=request.user,
            action="Play audio",
            detail=data.get('detail', ''),
            status=data.get('status', ''),
            client_type=f"{info['os']} / {info['browser']}",
            ip_address=server_ip,  
        )

        return JsonResponse({"message": "Log received"}, status=201)
    except Exception as e:
        UserLog.objects.create(
            user=request.user,
            action="Play audio",
            detail={"error": str(e)},
            status="error",
            client_type=f"{info['os']} / {info['browser']}",
            ip_address=server_ip,  
        )
        
        return JsonResponse({"error": str(e)}, status=400)

@require_POST
def ApiLogSaveFile(request):
    try:
        data = json.loads(request.body)
        detail = data.get('detail', '')
        info = get_user_os_browser_architecture(request)
        UserLog.objects.create(
            user=request.user,
            action="Save file",
            detail=detail,
            status="success",
            client_type=f"{info['os']} / {info['browser']}",
            ip_address=server_ip
        )
        return JsonResponse({"status": "ok"})
    except Exception as e:
        try:
            info = get_user_os_browser_architecture(request)
            UserLog.objects.create(
                user=request.user,
                action="Save file",
                detail={"error": str(e)},
                status="error",
                client_type=f"{info['os']} / {info['browser']}",
                ip_address=server_ip
            )
        except Exception:
            # swallow secondary errors when logging fails
            pass
        return JsonResponse({"status": "error", "message": str(e)}, status=400)