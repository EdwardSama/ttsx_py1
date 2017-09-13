from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator,Page


# Create your views here.


def index(request):
    type1 = GoodsInfo.objects.filter(gtype_id=1).order_by('-id')[0:4]
    type11= GoodsInfo.objects.filter(gtype_id=1).order_by('-gclick')[0:3]
    type2 = GoodsInfo.objects.filter(gtype_id=2).order_by('-id')[0:4]
    type22 = GoodsInfo.objects.filter(gtype_id=2).order_by('-gclick')[0:3]
    type3 = GoodsInfo.objects.filter(gtype_id=3).order_by('-id')[0:4]
    type33 = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[0:3]
    type4 = GoodsInfo.objects.filter(gtype_id=4).order_by('-id')[0:4]
    type44 = GoodsInfo.objects.filter(gtype_id=4).order_by('-gclick')[0:3]
    type5 = GoodsInfo.objects.filter(gtype_id=5).order_by('-id')[0:4]
    type55 = GoodsInfo.objects.filter(gtype_id=5).order_by('-gclick')[0:3]
    type6 = GoodsInfo.objects.filter(gtype_id=6).order_by('-id')[0:4]
    type66 = GoodsInfo.objects.filter(gtype_id=6).order_by('-gclick')[0:3]
    context={'type1':type1,'type2':type2,'type3':type3,'type4':type4,'type5':type5,'type6':type6,
             'type11':type11,'type22':type22,'type33':type33,'type44':type44,'type55':type55,'type66':type66}
    return render(request, 'tt_goods/index.html',context)



def list(request,sort,style,pindex):
    if int(style) == 1:
        good_list = GoodsInfo.objects.filter(gtype_id=sort).order_by('id')
    elif int(style)==2:
        good_list = GoodsInfo.objects.filter(gtype_id=sort).order_by('-gprice')
    elif int(style) ==3:
        good_list = GoodsInfo.objects.filter(gtype_id=sort).order_by('-gclick')
    tuijian = GoodsInfo.objects.filter(gtype_id=sort).order_by('-id')[0:2]
    fenlei = TypeInfo.objects.filter(id=sort)[0]
    p = Paginator(good_list,14)
    if pindex=='':
        pindex=1
    list2 = p.page(pindex)
    context = {"list":list2,'sort':sort,'style':style,'pindex':pindex,'tuijian':tuijian,'fenlei':fenlei}
    return render(request,'tt_goods/list.html',context)



def detail(request,id1,id2):
    type = TypeInfo.objects.filter(id=id1)
    good = GoodsInfo.objects.filter(id=id2)
    tuijian = GoodsInfo.objects.filter(gtype_id=id1).order_by('-id')[0:2]
    context={'good':good[0],'type':type[0],'tuijian':tuijian}
    return render(request,'tt_goods/detail.html',context)