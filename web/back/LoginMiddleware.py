from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
import re

class LoginCheck:


    def __init__(self, get_response):
        self.get_response = get_response
        # 一次性配置和初始化。

    def __call__(self, request):

        # pass
        # 后台登录页面的校验
        backpath = ['/admin/login.html']
        print(request.path)
        if re.match('/admin/',request.path) and request.path not in backpath:
            pass
            # if not request.session.get('_auth_user_id',None):
                # return HttpResponseRedirect(reverse('back_login'))
        # 前台登录页面校验
        passpath = ['/uc/','/pay/','/cart/']

        if (re.match('/uc/',request.path) or re.match('/cart/',request.path)) or request.path in passpath:
            if not request.session.get('vipuser'):
                return render(request,'home/login.html')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


























