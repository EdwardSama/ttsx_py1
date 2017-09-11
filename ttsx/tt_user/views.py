from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import *
import re
import hashlib

# Create your views here.

def register(request):

    return render(request,'tt_user/register.html')


def register_handle(request):
    dict = request.POST

    uname=dict.get('user_name')
    upwd = dict.get('pwd')
    cpwd = dict.get('cpwd')
    uemail = dict.get('email')

    if len(uname)>5 and len(uname)<20 and len(upwd)>8 and len(upwd)<20:

        if cpwd!=upwd:
            redirect('/user/register/')

        sha1 = hashlib.sha1()
        upwd = upwd.encode('utf-8')
        sha1.update(upwd)
        upwd = sha1.hexdigest()
        user = UserInfo.adduser.create(uname,upwd,uemail)
        user.save()

        return redirect('/user/login/')
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

    if len(user_info)==1:
        if user_info[0].isActive==False:
            if user_info[0].upwd == upwd :
                res = HttpResponseRedirect('/user/info/')
                if check!=0:
                    res.set_cookie('uname',uname)
                else:
                    res.set_cookie('uname','',max_age=-1)
                request.session['user_id']=user_info[0].id
                request.session['uname']=uname
                return res
            else:
                context={'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
                return render(request,'tt_user/login.html',context)
    else:
        context={'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request, 'tt_user/login.html', context)



def info(request):
    try:
        user_id = request.session['user_id']
        user = UserInfo.adduser.filter(id=user_id)
    except:
        return redirect('/user/login/')
    if len(user)==1:
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



def order(request):
    try:
        user_id = request.session['user_id']
        user = UserInfo.adduser.filter(id=user_id)
    except:
        return redirect('/user/login/')
    if len(user) == 1:
        return render(request, 'tt_user/user_center_order.html')



def site(request):
    try:
        user_id = request.session['user_id']
        user = UserInfo.adduser.filter(id=user_id)
    except:
        return redirect('/user/login/')
    if len(user) == 1:

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





def index(request):
    try:
        user_id = request.session['user_id']
        user = UserInfo.adduser.filter(id=user_id)
        uname = user[0].uname
        context = {'uname':uname}
        return render(request, 'index.html',context)
    except:
        return render(request,'index.html')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.adduser.filter(uname=uname).count()
    return JsonResponse({'count':count})









