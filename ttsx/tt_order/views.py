from django.shortcuts import render,redirect
from tt_user.decorater import islogin
from tt_user.models import *
from tt_cart.models import *
from .models import *
from django.db import transaction
from datetime import datetime

# Create your views here.

@islogin
def index(request):
    cid = request.GET.getlist('cid')
    if len(cid)==0:
        return redirect('/cart/')
    u_id = request.session['user_id']
    u_addr = UserAddressInfo.objects.get(user_id = u_id)
    addr = u_addr.uaddress
    tel = u_addr.uphone
    name = u_addr.uname

    cart = CartInfo.objects.filter(id__in=cid)
    num = len(cid)
    context={'clist':cart,'addr':addr,'tel':tel,'name':name,'num':num}

    return render(request, 'tt_order/order.html',context)



@transaction.atomic
@islogin
def order(request):
    u_id = request.session['user_id']
    cid = request.POST.getlist('cid')
    addr = request.POST.get('addr')
    sid = transaction.savepoint()
    cart_list = CartInfo.objects.filter(id__in= cid)
    order = OrderInfo()
    order.user_id = u_id
    order.oid = '%s%s'%(datetime.now().strftime('%Y%m%d%H%M%S'),u_id)
    total = 0
    order.ototal=0
    order.oaddress = addr
    order.save()
    isOK=True
    for cart in cart_list:
        if cart.count < cart.goods.gkucun:
            detail = OrderDetailInfo()
            detail.goods = cart.goods
            detail.order = order
            detail.price = cart.goods.gprice
            detail.count = cart.count
            detail.save()
            total += detail.count * detail.price
            cart.goods.gkucun -= cart.count
            cart.goods.save()
            cart.delete()
        else:
            isOK=False
            break
    if isOK:
        order.ototal=total
        order.save()
        transaction.savepoint_commit(sid)
        return redirect('/user/order/')
    else:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')


