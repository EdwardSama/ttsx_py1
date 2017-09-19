from django.shortcuts import render,redirect
from django.http import JsonResponse
from tt_user.decorater import islogin
from .models import *

# Create your views here.

@islogin
def index(request):
    u_id = request.session['user_id']
    cart = CartInfo.objects.filter(user_id = u_id)
    context= {'clist':cart}
    return render(request,'tt_cart/cart.html',context)




def edit(request):
    cid = request.GET.get('cid')
    count = request.GET.get('count')
    cart = CartInfo.objects.get(id=cid)
    cart.count = count
    cart.save()
    return JsonResponse({'ok':1})




def add(request):
    uid = request.session.get('user_id','')
    if uid=='':
        return JsonResponse({'login':1})

    gid = request.GET.get('gid')
    count = request.GET.get('count')
    cart = CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if cart:
        cart[0].count+=int(count)
        cart[0].save()
    else:
        cart = CartInfo()
        cart.goods_id = gid
        cart.user_id = uid
        cart.count = count
        cart.save()
    count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'ok':1,'count':count})
    

def delcart(request):
    cid = request.GET.get('cid')
    cart = CartInfo.objects.get(id=cid)
    cart.delete()
    return JsonResponse({'ok':1})



def count(request):
    uid = request.session.get('user_id', '')
    count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'count': count})