from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
# Create your views here.
from django.utils.html import format_html
from ..models import Types,JsonExtendEncoder

import datetime,time,json


#栏目分类
def GetTree(data,pid):
    tree = []

    for k in data:
        if k['t_pid'] == pid:
            return tree.append(k)
        else:
            return GetTree(data,k['t_pid'])
    return tree

#查询条件
def getKwargs(data={}):
    kwargs = {}
    for (k , v)  in data.items() :
       if v is not None and v != u'' :
           kwargs[k] = v

    return kwargs
 #获取数据
def get_type_data(request):
    kwargs = getKwargs(request.GET)

    try:
        if 't_name' in kwargs:
            udate = kwargs['t_name']
            kwargs.pop('t_name')
            object = Types.objects.filter(Q(t_name__contains=udate)).filter(**kwargs).extra(
                select={'paths': 'concat(t_path,id)'}).order_by('paths').values()
        else:
            object = Types.objects.filter(**kwargs).extra(select={'paths': 'concat(t_path,id)'}).order_by(
                'paths').values()

    except:
        print(2)
        object = Types.objects.extra(select={'paths': 'concat(t_path,id)'}).order_by('paths').values()

    count = object.count()
    for k in object:

        if k['t_pid'] == 0:
            k['pid_name'] = '顶级栏目'
        else:
            k['pid_name'] = Types.objects.get(id=k['t_pid']).t_name

    data = json.dumps(list(object), cls=JsonExtendEncoder)

    datas = {}
    datas['code'] = 0
    datas['msg'] = ''
    datas['count'] = count
    datas['data'] = json.loads(data)

    return HttpResponse(json.dumps(datas))


#产品类别列表
def typelist(request):

    return render(request,'back/types/list.html')

#产品类别添加
def typeadd(request):
    if request.method == 'GET':

        types = Types.objects.extra(select={'paths': 'concat(t_path,id)'}).order_by('paths')
        for t in types:
            if t.t_pid == 0:
                t.pname = '顶级分类'
            else:
                obj = Types.objects.get(id=t.t_pid)
                t.pname = obj.t_name
                num = obj.t_path.count(',')
                t.t_name = (num * '&nbsp;&nbsp;&nbsp;&nbsp;') +'|&nbsp;&nbsp;'+t.t_name

        return render(request,'back/types/add.html',{'type':types})

    elif request.method == 'POST':
        try:
            object = Types()
            object.t_name = request.POST['t_name']
            object.t_pid = request.POST['t_pid']
            object.t_info = request.POST['t_info']
            object.t_isdel = 0
            if request.POST['t_pid'] == '0':
                object.t_path = '0,'
            else:
                obj = Types.objects.get(id = request.POST['t_pid'])
                object.t_path = '{p}{c},'.format(p = obj.t_path,c = request.POST['t_pid'])
            object.save()
            return JsonResponse({'code':1,'msg':'添加栏目成功'})
        except:
            return JsonResponse({'code':0,'msg':'添加栏目失败','href':reverse('typelist')})

        # return HttpResponse(1)

#产品类别详情
def typedetail(request):
    object = Types.objects.filter(id = request.GET.get('id')).values()
    for k in object:
        if k['t_pid'] == 0:
            k['pid_name'] = '顶级栏目'
        else:
            k['pid_name'] = Types.objects.filter(id = k['t_pid'])[0].t_name

    return render(request, 'back/types/detail.html',{'data':object[0]})

#产品类别修改
def typeedit(request):

    if request.method == 'GET':
        object = Types.objects.filter(id=request.GET.get('id')).values()
        type = Types.objects.all()
        return render(request, 'back/types/edit.html',{'data':object[0],'type':type})

    elif request.method == 'POST':
        try:
            object = Types.objects.get(id = request.POST['id'])
            object.t_name = request.POST['t_name']
            object.t_pid = request.POST['t_pid']
            object.t_info = request.POST['t_info']

            if request.POST['t_pid'] == '0':
                object.t_path = '0,'
            else:
                obj = Types.objects.get(id=int(request.POST['t_pid']))
                object.t_path = '{p}{c},'.format(p =obj.t_path ,c=request.POST['t_pid'])

            object.save()
            return JsonResponse({'code':1,'msg':'修改信息成功'})
        except:
            return JsonResponse({'code':0,'msg':'修改信息失败','href':reverse('typelist')})

        #return HttpResponse(0)


# 审核类别状态
def type_change_status(request):
    status  = request.POST.get('status')
    object = Types.objects.get(id = request.POST.get('id'))
    try:

        if status == '0':
            object.t_isdel = 1
        else:
            object.t_isdel = 0
        object.save()

        object = Types.objects.get(id=request.POST.get('id'))
        print(object.t_isdel)
        return JsonResponse({'code':1,'pid':object.t_isdel,'msg':'修改成功'})
    except:
        return JsonResponse({'code':0,'pid':object.t_isdel,'msg':'修改失败'})



#产品类别显示状态
def typedel(request):
    try:
        object = Types.objects.get(id = request.GET.get('id'))
        object.t_isdel = 0
        object.save()
        return JsonResponse({'code': 1, 'msg': '栏目删除成功'})
    except:
        return JsonResponse({'code': 0, 'msg': '栏目删除失败', 'href': reverse('typelist')})



