from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse

# Create your views here.


#后台首页
def back(request):

    return render(request,'back/index.html')


#后台登录
def back_login(request):
    if request.method == 'GET':
        return render(request,'back/login.html')
    elif request.method == 'POST':
        username = request.POST.get('account')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'code':1,'msg':'登陆成功','href':reverse('back')})

            return JsonResponse({'code':0,'msg':'登陆失败!账号或密码有误。'})
        except:
            return JsonResponse({'code':0,'msg':'登陆失败!账号或密码有误。'})
        #return HttpResponse(0)

#退出登录
def back_logout(request):
    logout(request)
    return  HttpResponseRedirect(reverse('back_login'))



