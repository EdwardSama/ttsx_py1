from django.shortcuts import redirect
from .models import *


def islogin(func):

    def wrapper(request):
        user_id = request.session.get('user_id','')
        if user_id=='':
            return redirect('/user/login/')
        else:
            return func(request)
    return wrapper