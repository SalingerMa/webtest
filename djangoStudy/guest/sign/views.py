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
    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page 不是整数，取第一页的数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不再范围内，取最后一页
        contacts = paginator.page(paginator.num_pages)
    context = {
        'user': username,
        'guests': contacts,
    }

    return render(request, "guest_manage.html", context)

# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    # 该发布会下的总人数
    allNum = len(Guest.objects.filter(event_id=eid))
    # 已签到的总人数
    signNum = len(Guest.objects.filter(event_id=eid, sign=True))
    context = {
        'event': event,
        'allNum': allNum,
        'signNum': signNum,
    }
    return render(request, 'sign_index.html', context)

# 签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    # 该发布会下的总人数
    allNum = len(Guest.objects.filter(event_id=eid))

    # 判断手机号是否存在
    result = Guest.objects.filter(phone=phone)
    if not result:
        signNum = len(Guest.objects.filter(event_id=eid, sign=True))
        context = {'event': event,
                   'hint': 'phone error.',
                   'allNum': allNum,
                   'signNum': signNum,
                }
        return render(request, 'sign_index.html', context)

    # 通过手机号和发布会ID来判断两者之间是否匹配
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        signNum = len(Guest.objects.filter(event_id=eid, sign=True))
        context = {'event': event,
                   'hint': 'event id or phone error.',
                   'allNum': allNum,
                   'signNum': signNum,
                   }
        return render(request, 'sign_index.html', context)

    # 判断嘉宾的签到状态，根据状态进行修改
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        signNum = len(Guest.objects.filter(event_id=eid, sign=True))
        context = {'event': event,
                   'hint': 'user has sign in.',
                   'allNum': allNum,
                   'signNum': signNum,
                   }
        return render(request, "sign_index.html", context)
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign=1)
        signNum = len(Guest.objects.filter(event_id=eid, sign=True))
        context = {'event': event,
                   'hint': 'sign in success!.',
                   'allNum': allNum,
                   'signNum': signNum,
                   }
        return render(request, 'sign_index.html', context)


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response