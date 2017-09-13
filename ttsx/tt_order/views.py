from django.shortcuts import render

# Create your views here.
def order(request):
    provice='江西省'
    city='景德镇市'
    area='浮梁县洪源镇'
    name='邹家俊'
    tel='17304437532'
    context={'provice':provice,'city':city,'area':area,'name':name,'tel':tel}
    return render(request,'tt_order/place_order.html',context)

def center(request):
    return render(request, 'tt_order/user_center_info.html')


