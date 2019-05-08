from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
# Create your views here.
from django.utils.html import format_html
from ..models import Orders,Address,Users,OrderDetail,Goods,JsonExtendEncoder

import datetime,time,json,random,shutil,os
from django.conf import settings
# Create your views here.


#获取订单数据
def order_getdata(request):
    #分页
    limit = int(request.GET.get('limit',20))
    page = int(request.GET.get('page',1))
    start = (page-1) * limit
    end = limit * page

    object = Orders.objects.all().order_by('-id')[start:end].values()
    for v in object:
        v['o_totalprice'] = v['o_totalprice'].to_eng_string()
        v['o_totalnum'] = v['o_totalnum']
        v['o_address'] = Address.objects.get(id = v['o_address_id']).u_address
        v['o_user'] = Users.objects.get(id = v['o_uid_id']).username

    obj = json.dumps(list(object), cls=JsonExtendEncoder, ensure_ascii=False)
    datas={}
    datas['code']=0
    datas['msg'] = ''
    datas['count'] = Orders.objects.all().count()
    datas['data'] = json.loads(obj)
    return HttpResponse(json.dumps(datas))
    #return HttpResponse(0)


#获取订单数据
def orderdetail_getdata(request):
    #分页
    limit = int(request.GET.get('limit',10))
    page = int(request.GET.get('page',1))
    start = (page-1) * limit
    end = limit * page

    object = OrderDetail.objects.filter(id = request.GET.get('id')).order_by('-id')[start:end].values()
    for v in object:
        v['o_totalprice'] = v['o_totalprice'].to_eng_string()
        v['o_totalnum'] = v['o_totalnum']
        v['o_address'] = Address.objects.get(id = v['o_address_id']).u_address
        v['o_user'] = Users.objects.get(id = v['o_uid_id']).username

    obj = json.dumps(list(object), cls=JsonExtendEncoder, ensure_ascii=False)
    datas={}
    datas['code']=0
    datas['msg'] = ''
    datas['count'] = OrderDetail.objects.filter(id = request.GET.get('id')).count()
    datas['data'] = json.loads(obj)
    print(request.GET.get('id'))
    return HttpResponse(json.dumps(datas))
    #return HttpResponse(0)

#订单列表
def order_list(request):

    return render(request,'back/order/list.html')

#订单详情
def order_detail(request):
    #分页
    limit = int(request.GET.get('limit',10))
    page = int(request.GET.get('page',1))
    start = (page-1) * limit
    end = limit * page

    object = OrderDetail.objects.filter(d_oid = request.GET.get('id')).order_by('-id')[start:end].values()

    for v in object:
        v['name'] = Goods.objects.get(id=v['d_gid_id']).g_name
        v['price'] = Goods.objects.get(id=v['d_gid_id']).g_price.to_eng_string()
        v['saleprice'] = Goods.objects.get(id=v['d_gid_id']).g_saleprice.to_eng_string()
        v['mall'] = Goods.objects.get(id=v['d_gid_id']).g_mall
        v['type'] = Goods.objects.get(id=v['d_gid_id']).g_type
    obj = json.dumps(list(object), cls=JsonExtendEncoder, ensure_ascii=False)
    return render(request,'back/order/detail.html',{'data':obj})

#订单状态修改
def order_edit(request):
    if request.method == 'GET':
        data = Orders.objects.get(id=request.GET.get('id'))

        return render(request,'back/order/edit.html',{'data':data})
    elif request.method == 'POST':
        try:
            object = Orders.objects.get(id = request.POST.get('id'))
            object.o_status = int(request.POST.get('status'))
            object.save()
            return JsonResponse({'code':1,'msg':'修改成功'})
        except:
            return JsonResponse({'code':0,'msg':'修改失败'})


