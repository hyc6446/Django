from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
# Create your views here.
from django.utils.html import format_html
from ..models import Users,JsonExtendEncoder

import datetime,time,json

#查询条件
def getKwargs(data={}):
   kwargs = {}
   for (k , v)  in data.items() :
       if v is not None and v != u'' :
           kwargs[k] = v
   return kwargs

#会员列表
def userlist(request):
    search = request.GET
    kwargs = getKwargs(search)

    try:
        if 'u_addtime' in kwargs:
            udate = kwargs['u_addtime']
            kwargs.pop('u_addtime')
            object = Users.objects.filter(Q(u_addtime__contains=udate)).filter(**kwargs).values()
        else:
            object = Users.objects.filter(**kwargs).values()
        count = object.count()
    except Users.DoesNotExist:
        object = Users.objects.all().values()
        count = object.count()


    for k in object:
        k['level_name'] = Users.objects.get(id=k['id']).u_level.l_name
    data = json.dumps(list(object), cls=JsonExtendEncoder)

    return render(request,'back/user/list.html',{'data':data,'count':count})

#会员查看
def detail(request):

    id= request.GET.get('id')
    data = Users.objects.get(id=id)

    return render(request,'back/user/detail.html',{'data':data})

#审核会员
def changestatus(request):

    id = request.GET.get('id')
    stacode = request.GET.get('status')
    if stacode == 'true':
        stacode = '已审核'
    else:
        stacode = '未审核'

    try:
        object=Users.objects.get(id=id)
        object.u_status = stacode
        object.save()
        stacode = object.u_status
        return JsonResponse({'code':1,'stacode':stacode,'msg':'审核成功'})
    except:
        return JsonResponse({'code': 0, 'stacode': stacode,'msg':'审核失败'})

















