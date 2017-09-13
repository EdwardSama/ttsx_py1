from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator

# Create your views here.


def list(request, tid, pindex, sort):
    typeinfo = TypeInfo.objects.get(pk=tid)
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]

    if int(sort) == 1:
        goods_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-id')
    elif int(sort) == 2:
        goods_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-gprice')
    else:
        goods_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-gclick')


    p = Paginator(goods_list, 15)

    page = p.page(pindex)

    context = {'title': typeinfo.ttitle, 'guest_cart': 1,
               'news': news,
               'page': page,
               'paginator': p,
               'typeinfo': typeinfo,
               'sort': sort
               }
    return render(request, 'ttsx_goods/list.html', context)


def detail(request, id):
    goods = GoodsInfo.objects.get(pk=id)
    goods.gclick += 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title':goods.gtype.ttitle,'goods':goods,
        'news':news,'id':id
    }
    return render(request, 'ttsx_goods/detail.html',context)


def index(request):
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4],
    type00 = typelist[0].goodsinfo_set.order_by('-gclick')[0:3],
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4],
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:3],
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4],
    type22 = typelist[2].goodsinfo_set.order_by('-gclick')[0:3],
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4],
    type33 = typelist[3].goodsinfo_set.order_by('-gclick')[0:3],
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4],
    type44 = typelist[4].goodsinfo_set.order_by('-gclick')[0:3],
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4],
    type55 = typelist[5].goodsinfo_set.order_by('-gclick')[0:3],
    context = {'title': '首页', 'guest_cart': 1,
               'type0': (type0[0])[0:4], 'type00': type00[0],
               'type1': type1[0], 'type11': type11[0],
               'type2': type2[0], 'type22': type22[0],
               'type3': type3[0], 'type33': type33[0],
               'type4': type4[0], 'type44': type44[0],
               'type5': type5[0], 'type55': type55[0],
               }
    return render(request, 'ttsx_goods/index.html', context)
