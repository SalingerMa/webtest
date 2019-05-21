from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')


        """
         # authenticate函数认证给定的用户名个密码。
         它接收用户名和密码两个参数，并且会在用户名和密码正确的情况下返回一个user对象
         否则返回None
        """
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username  # 将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')

            return response
        else:
            context = {
                'error': 'username or password error'
            }
            return render(request, 'index.html', context)

@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')  # 读取浏览器session

    context = {
        'user': username,
        'events': event_list,
    }
    return render(request, "event_manage.html", context)


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    # search_name_bytes = search_name.encode(encoding="utf-8")
    # event_list = Event.objects.filter(name__contains=search_name_bytes)
    event_list = Event.objects.filter(name__contains=search_name)
    context = {
        "user": username,
        "events": event_list,
    }
    return render(request, "event_manage.html", context)

# 嘉宾管理
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('user', '')
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context = {
        'user': username,
        'guests': contacts,
    }

    return render(request, "guest_manage.html",context)

# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    print(event)
    # guest_list = Guest.objects.filter(event_id=eid)           # 签到人数
    # sign_list = Guest.objects.filter(sign="1", event_id=eid)   # 已签到数
    # guest_data = str(len(guest_list))
    # sign_data = str(len(sign_list))
    context = {
        'event': event,
        # 'guest': guest_data,
        # 'sign': sign_data
    }
    return render(request, 'sign_index.html', context)
