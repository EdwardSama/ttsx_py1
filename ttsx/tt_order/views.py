from django.shortcuts import render

# Create your views here.
def order(request):
    return render(request,'tt_order/place_order.html')