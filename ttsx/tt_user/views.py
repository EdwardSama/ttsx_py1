from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *
import re
import hashlib
from .decorater import islogin
from . import task
from tt_goods.models import *
from tt_order.models import *
from django.core.paginator import Paginator


#Create your views here.

def register(request):
    return render(request, 'tt_user/register.html')


def register_handle(request):
    dict = request.POST
    uname = dict.get('user_name','')
    upwd = dict.get('pwd', '')
    cpwd = dict.get('cpwd', '')
    uemail = dict.get('email', '')
    e_uemail = re.compile('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$')
    e_flag = e_uemail.match(uemail)
    n_uname = re.compile('^[a-z0-9_][\w]{4,19}$')
    n_flag = n_uname.match(uname)
    p_upwd = re.compile('^[a-z0-9][\w]{7,19}$')
    p_flag = p_upwd.match(upwd)
    if e_flag and n_flag and p_flag and cpwd == upwd:
        sha1 = hashlib.sha1()
        upwd = upwd.encode('utf-8')
        sha1.update(upwd)
        upwd = sha1.hexdigest()
        user = UserInfo.adduser.create(uname, upwd, uemail)
        user.save()
        task.sendmail.delay(uemail, uname)
        return render(request, 'tt_user/active.html')
    else:
        return redirect('/user/register/')


def login(request):
    uname = request.COOKIES.get('uname', 0)
    context = {'uname': uname}
    return render(request, 'tt_user/login.html', context)


def login_handle(request):
    dict = request.POST
    uname = dict.get('username', '')
    upwd = dict.get('pwd', '')
    check = dict.get('jizhu', 0)
    if uname and upwd:
        sha1 = hashlib.sha1()
        upwd = upwd.encode('utf-8')
        sha1.update(upwd)
        upwd = sha1.hexdigest()
    user_info = UserInfo.adduser.filter(uname=uname)
    url = request.session.get('url_path', '/')
    if len(user_info) == 1:
        if user_info[0].isActive == True:
            if user_info[0].upwd == upwd:
                res = HttpResponseRedirect(url)
                if check != 0:
                    res.set_cookie('uname', uname,max_age=60*60*24*14)
                else:
                    res.set_cookie('uname', '', max_age=-1)
                request.session['user_id'] = user_info[0].id
                request.session['uname'] = uname
                return res
            else:
                context = { 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd, 'active': 1}
                return render(request, 'tt_user/login.html', context)
        else:
            context = {'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd, 'active': 0}
            return render(request, 'tt_user/login.html', context)
    else:
        context = {'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd, 'active': 1}
        return render(request, 'tt_user/login.html', context)


@islogin
def info(request):
    good_list = []
    goods_ids = request.COOKIES.get('goods_ids', '')
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        for good_id in goods_ids1:
            good = GoodsInfo.objects.get(id=int(good_id))
            good_list.append(good)
    user_id = request.session['user_id']
    user = UserInfo.adduser.filter(id=user_id)
    email = user[0].uemail
    uname = user[0].uname
    try:
        user_addr = UserAddressInfo.objects.filter(user_id=user_id)
        addr = user_addr[0].uaddress
        context = {'email': email, 'uname': uname, 'addr': addr, 'g_list': good_list}
        return render(request, 'tt_user/user_center_info.html', context)
    except:
        context = {'email': email, 'uname': uname, 'addr': '尚未填写', 'g_list': good_list}
        return render(request, 'tt_user/user_center_info.html', context)


@islogin
def order(request,pindex):
    if pindex=='':
        pindex=1
    user_id = request.session['user_id']
    order = OrderInfo.objects.filter(user=user_id)
    p = Paginator(order,2)
    order = p.page(pindex)
    context = {'order': order}
    return render(request, 'tt_user/user_center_order.html', context)


@islogin
def site(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        dict = request.POST
        name = dict.get('name', '')
        addr = dict.get('addr', '')
        mail = dict.get('mail', '')
        tel = dict.get('tel', '')
        if name and addr and mail and tel:
            user_addr = UserAddressInfo()
            if UserAddressInfo.objects.filter(user_id=user_id):
                UserAddressInfo.objects.get(user_id=user_id).delete()
            user_addr.user_id = user_id
            user_addr.uname = name
            user_addr.uaddress = addr
            user_addr.uphone = tel
            user_addr.save()
            context = {'name': name, 'addr': addr, 'mail': mail, 'tel': tel}
            return render(request, 'tt_user/user_center_site.html', context)
        else:
            user_addr = UserAddressInfo.objects.filter(user_id=user_id)
            user_info = UserInfo.adduser.filter(id=user_id)
            try:
                name = user_addr[0].uname
                addr = user_addr[0].uaddress
                mail = user_info[0].uemail
                tel = user_addr[0].uphone
                context = {'name': name, 'addr': addr, 'mail': mail, 'tel': tel}
                return render(request, 'tt_user/user_center_site.html', context)
            except:
                context = {'name': '尚未填写', 'addr': '尚未填写', 'mail': '尚未填写', 'tel': '尚未填写'}
                return render(request, 'tt_user/user_center_site.html', context)
    else:
        user_addr = UserAddressInfo.objects.filter(user_id=user_id)
        user_info = UserInfo.adduser.filter(id=user_id)
        try:
            name = user_addr[0].uname
            addr = user_addr[0].uaddress
            mail = user_info[0].uemail
            tel = user_addr[0].uphone
            context = {'name': name, 'addr': addr, 'mail': mail, 'tel': tel}
            return render(request, 'tt_user/user_center_site.html', context)
        except:
            context = {'name': '尚未填写', 'addr': '尚未填写', 'mail': '尚未填写', 'tel': '尚未填写'}
            return render(request, 'tt_user/user_center_site.html', context)


def login_out(request):
    request.session.flush()
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.adduser.filter(uname=uname).count()
    return JsonResponse({'count': count})


def active(request):
    uname = request.GET.get('uname', '')
    if uname != '':
        user = UserInfo.adduser.get(uname=uname)
        user.isActive = True
        user.save()
        return redirect('/user/login/')

@islogin
def pay(request):
    id = request.POST.get('id')
    order = OrderInfo.objects.get(pk=id)
    order.oIsPay=True
    order.save()
    return redirect('/user/order/')

