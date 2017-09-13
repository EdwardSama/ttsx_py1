from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import *
import re
import hashlib
from .decorater import islogin
from . import task

# Create your views here.

def register(request):

    return render(request,'tt_user/register.html')


def register_handle(request):
    dict = request.POST
    uname=dict.get('user_name','')
    upwd = dict.get('pwd','')
    cpwd = dict.get('cpwd','')
    uemail = dict.get('email','')
    e_uemail = re.compile('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$')
    e_flag=e_uemail.match(uemail)
    n_uname=re.compile('^[a-z0-9_][\w]{4,19}$')
    n_flag = n_uname.match(uname)
    p_upwd = re.compile('^[a-z0-9][\w]{7,19}$')
    p_flag = p_upwd.match(upwd)

    if e_flag and n_flag and p_flag  and cpwd==upwd:

        sha1 = hashlib.sha1()
        upwd = upwd.encode('utf-8')
        sha1.update(upwd)
        upwd = sha1.hexdigest()
        user = UserInfo.adduser.create(uname,upwd,uemail)
        user.save()
        task.sendmail.delay(uemail,uname)

        return render(request,'tt_user/active.html')
    else:
        return redirect('/user/register/')



def login(request):

    return render(request,'tt_user/login.html')




def login_handle(request):
    dict = request.POST
    uname = dict.get('username','')
    upwd = dict.get('pwd','')
    check = dict.get('jizhu',0)
    if uname and upwd:
        sha1 = hashlib.sha1()
        upwd = upwd.encode('utf-8')
        sha1.update(upwd)
        upwd = sha1.hexdigest()

    user_info = UserInfo.adduser.filter(uname=uname)
    url = request.session.get('url_path','/')
    print(url)

    if len(user_info)==1:
        if user_info[0].isActive==True:
            if user_info[0].upwd == upwd :
                res = HttpResponseRedirect(url)
                if check!=0:
                    res.set_cookie('uname',uname)
                else:
                    res.set_cookie('uname','',max_age=-1)
                request.session['user_id']=user_info[0].id
                request.session['uname']=uname
                return res
            else:
                context={'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd,'active':1}
                return render(request,'tt_user/login.html',context)
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd, 'active':0}
            return render(request, 'tt_user/login.html', context)
    else:
        context={'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd,'active':1}
        return render(request, 'tt_user/login.html', context)


@islogin
def info(request):
    user_id = request.session['user_id']
    user = UserInfo.adduser.filter(id=user_id)
    email = user[0].uemail
    uname = user[0].uname
    try:
        user_addr = UserAddressInfo.objects.filter(user_id=user_id)
        addr = user_addr[0].uaddress
        context = {'email':email,'uname':uname,'addr':addr}
        return render(request,'tt_user/user_center_info.html',context)
    except:
        context = {'email': email, 'uname': uname,'addr':'尚未填写'}
        return render(request, 'tt_user/user_center_info.html', context)


@islogin
def order(request):

    return render(request, 'tt_user/user_center_order.html')


@islogin
def site(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        dict = request.POST
        name = dict.get('name')
        addr = dict.get('addr')
        mail = dict.get('mail')
        tel = dict.get('tel')
        user_addr = UserAddressInfo()
        user_addr.user_id=user_id
        user_addr.uname=name
        user_addr.uaddress=addr
        user_addr.uphone=tel
        user_addr.save()
        context = {'name':name , 'addr':addr ,'mail':mail,'tel':tel}
        return render(request,'tt_user/user_center_site.html',context)
    else:
        user_addr=UserAddressInfo.objects.filter(user_id=user_id)
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
    return JsonResponse({'count':count})


def active(request):
    uname=request.GET.get('uname','')
    if uname != '':
        user=UserInfo.adduser.get(uname=uname)
        user.isActive=True
        user.save()
        return redirect('/user/login/')










