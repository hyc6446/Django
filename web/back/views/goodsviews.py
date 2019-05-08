from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
# Create your views here.
from django.utils.html import format_html
from ..models import Types,GoodsAttr,Goods,Pictures,GoodsInfo,JsonExtendEncoder

import datetime,time,json,random,shutil,os
from django.conf import settings
import os


#查询条件
def getKwargs(data={}):
   kwargs = {}
   for (k , v)  in data.items() :
       if v is not None :
           kwargs[k] = v
   return kwargs

#获取数据返回json格式
def gettype(request):

    object = GoodsAttr.objects.all().values()

    for i in object:
        if i['a_pid'] == 0:
            i['pid_name'] = '顶级属性'
        else:
            i['pid_name'] = GoodsAttr.objects.get(id = i['a_pid']).a_name
    obj = json.dumps(list(object), cls=JsonExtendEncoder, ensure_ascii=False)
    datas={}
    datas['code']=0
    datas['msg'] = ''
    datas['count'] = object.count()
    datas['data'] = json.loads(obj)
    return HttpResponse(json.dumps(datas))


#商品属性列表
def goods_trait_list(request):

    return render(request,'back/trait/list.html')

#商品属性添加
def goods_trait_add(request):
    if request.method == 'GET':
        type = GoodsAttr.objects.filter(a_pid = 0)

        return render(request,'back/trait/add.html',{'type':type})

    elif request.method == 'POST':
        try:
            object = GoodsAttr()
            object.a_name = request.POST.get('a_name')
            object.a_pid = request.POST.get('a_pid',0)
            object.a_info = request.POST.get('a_info','暂无简介')
            if request.POST['a_pid'] == '0':
                object.a_path = '0,'
            else:
                obj = GoodsAttr.objects.get(id = request.POST['a_pid'])
                object.a_path = '{p}{c},'.format(p = obj.a_path,c = request.POST['a_pid'])
            object.a_isdel = 1

            object.save()
            return JsonResponse({'code': 1, 'msg': '添加属性成功','href':reverse(goods_trait_list)})
        except:
            return JsonResponse({'code': 0, 'msg': '添加属性失败','href':reverse(goods_trait_list)})

#商品属性修改
def goods_trait_edit(request):
    if request.method == 'GET':
        data = GoodsAttr.objects.get(id = request.GET.get('id'))
        type = GoodsAttr.objects.filter(a_pid=0)
        return render(request,'back/trait/edit.html',{'data':data,'type':type})
    elif request.method == 'POST':

        try:
            object = GoodsAttr.objects.get(id = request.POST['id'])
            object.a_name = request.POST['a_name']
            object.a_info = request.POST['a_info']
            object.a_isdel = request.POST['a_isdel']

            object.save()
            return JsonResponse({'code': 1, 'msg': '修改属性成功'})
        except:
            return JsonResponse({'code': 0, 'msg': '修改属性失败'})


#获取商品数据返回json格式
def getgoods(request):

    #分页
    limit = int(request.GET.get('limit',20))
    page = int(request.GET.get('page',1))
    start = (page-1) * limit
    end = limit * page

    object = Goods.objects.all().order_by('-id')[start:end].values()
    for v in object:
        v['g_price'] = v['g_price'].to_eng_string()
        v['g_saleprice'] = v['g_saleprice'].to_eng_string()
        v['t_name'] = Types.objects.get(id = v['g_tid_id']).t_name
    obj = json.dumps(list(object), cls=JsonExtendEncoder, ensure_ascii=False)
    datas={}
    datas['code']=0
    datas['msg'] = ''
    datas['count'] = Goods.objects.all().count()
    datas['data'] = json.loads(obj)
    return HttpResponse(json.dumps(datas))

#所有商品列表
def goodslist(request):

    return render(request,'back/goods/list.html')


#商品添加、商品修改的公用数据
def getcontext():
    types = Types.objects.extra(select={'paths': 'concat(t_path,id)'}).order_by('paths')
    for t in types:
        if t.t_pid == 0:
            t.pname = '顶级分类'
        else:
            obj = Types.objects.get(id=t.t_pid)
            t.pname = obj.t_name
            num = obj.t_path.count(',')
            t.t_name = (num * '|----') + t.t_name

    # 颜色属性
    color = GoodsAttr.objects.get(a_pid=0, a_name='颜色')
    cid = color.id
    color_sub = GoodsAttr.objects.filter(a_pid=cid).extra(select={'paths': 'concat(a_path,id)'}).order_by('paths')
    # 尺寸属性
    size = GoodsAttr.objects.get(a_pid=0, a_name='尺寸')
    sid = size.id
    size_sub = GoodsAttr.objects.filter(a_pid=sid).extra(select={'paths': 'concat(a_path,id)'}).order_by('paths')

    context = {'types': types, 'color': color_sub, 'size': size_sub}

    return context

#商品添加
def goodsadd(request):
    if request.method == 'GET':

        context = getcontext()

        return render(request,'back/goods/add.html',context)

    elif request.method == 'POST':
        try:
            #data = request.POST.copy().dict()
            data = getKwargs(request.POST)
            # del data['csrfmiddlewaretoken']
            if data['g_isdel'] == 'on':
                data['g_isdel'] = 1
            else:
                data['g_isdel'] = 0
            #添加商品信息
            obj = Goods()
            obj.g_price = data['g_price']
            obj.g_isdel = data['g_isdel']
            obj.g_saleprice = data['g_saleprice']
            obj.g_type = data['g_type']
            obj.g_address = data['provid']+','+data['cityid']+','+data['areaid']
            obj.g_tid = Types.objects.get(id= int(data['g_tid']))
            obj.g_name = data['g_name']
            obj.g_title = data.get('g_title')
            obj.g_intro = data.get('g_intro')
            obj.g_mall = data['g_mall']
            obj.g_nums = data['g_nums']
            obj.g_invnum = data['g_nums']
            #print(obj.g_price,obj.g_isdel,obj.g_saleprice,obj.g_type,obj.g_address,obj.g_tid,obj.g_name,obj.g_title,obj.g_intro,obj.g_mall,obj.g_nums)
            obj.save()
            #添加商品属性
            info = GoodsInfo()
            info.i_info = data['i_info']
            info.i_color = data['i_color']
            info.i_size = data['i_size']
            info.i_pinpai = data['i_pinpai']
            info.i_gid = obj

            info.save()
            #添加商品图片
            if data['p_pic']:
                print(data['p_pic'])
                getpics = data['p_pic'].split(',')
                if getpics:
                    for p in getpics:
                        pic = Pictures()
                        pic.p_gid = obj
                        pic.p_name = data['g_name']
                        pic.p_pic = p.replace("/media/images/goods/cache/", "/media/images/goods/")

                        pic.save()
                        shutil.move(settings.BASE_DIR+p,settings.BASE_DIR+'/media/images/goods/')

            return JsonResponse({'code':1,'msg':'商品添加成功'})
        except:
            return JsonResponse({'code':0,'msg':'商品添加失败'})

        #return HttpResponse(0)


#商品图片
def goodspicture(request):

    data = Pictures.objects.filter(p_gid_id=request.GET.get('id')).order_by('-p_addtime')


    return render(request,'back/goods/picture.html',{'data':data})

#商品图片删除
def pics_del(request):

    try:
        obj = Pictures.objects.get(id = request.GET.get('id'))
        obj.p_isdel = 0
        obj.save()
        return JsonResponse({'code':1,'msg':'删除成功'})
    except:
        return JsonResponse({'code':0,'msg':'删除失败'})


#商品编辑
def goodsedit(request):

    if request.method == 'GET':
        data = Goods.objects.get(id=request.GET.get('id'))
        context = getcontext()
        context['data'] = data
        return render(request,'back/goods/edit.html',context)

    elif request.method == 'POST':
        try:
            #data = request.POST.copy().dict()
            data = getKwargs(request.POST)
                # del data['csrfmiddlewaretoken']
            #修改商品信息
            obj = Goods.objects.get(id=int(request.POST.get('id')))
            obj.g_address = data['provid']+','+data['cityid']+','+data['areaid']
            obj.g_tid = Types.objects.get(id= data['g_tid'])
            obj.g_name = data['g_name']
            obj.g_price = data['g_price']
            obj.g_saleprice = data['g_saleprice']
            obj.g_title = data.get('g_title')
            obj.g_intro = data.get('g_intro')
            obj.g_isdel = int(data['g_isdel'])
            obj.g_mall = data['g_mall']
            obj.g_nums = data['g_nums']
            obj.g_type = data['g_type']

            #print(data['p_cover'],obj.g_price,obj.g_isdel,obj.g_saleprice,obj.g_type,obj.g_address,obj.g_tid,obj.g_name,obj.g_title,obj.g_intro,obj.g_mall,obj.g_nums)
            obj.save()

            #修改商品属性
            info = GoodsInfo.objects.get(id = int(request.POST.get('id')))
            info.i_info = data['i_info']
            info.i_color = data['i_color']
            info.i_size = data['i_size']
            info.i_pinpai = data['i_pinpai']
            info.i_gid = obj

            info.save()
            #修改商品图片
            if data['p_cover']:
                pic = Pictures.objects.get(id = int(data['p_cover']))
                pic.p_cover = 1
                pic.save()

            # 上传商品图片
            if data['p_pic']:
                getpics = data['p_pic'].split(',')
                if getpics:
                    for p in getpics:
                        pic = Pictures()
                        pic.p_gid = obj
                        pic.p_name = data['g_name']
                        pic.p_pic = p.replace("/media/images/goods/cache/", "/media/images/goods/")
                        pic.save()
                        if not str(settings.BASE_DIR)+pic.p_pic:
                            shutil.move(settings.BASE_DIR+p,settings.BASE_DIR+'/media/images/goods/')

            return JsonResponse({'code':1,'msg':'商品添加成功'})
        except:
            return JsonResponse({'code':0,'msg':'商品添加失败'})
        #return HttpResponse(0)

#商品详情
def goodsdetail(request):

    data = Goods.objects.get(id = request.GET.get('id'))

    return render(request,'back/goods/detail.html',{'data':data})

#商品回收站
def goodstrash(request):

    return render(request,'back/public/message.html')



#==================================================================
#修改商品状态

def goods_status(request):

    return HttpResponse(0)


#商品详情图片上传视图
def goodsupload(request):
    getfile = request.FILES.get('file')
    try:
        if getfile:
            aa = upload_goods_con(request)

            return JsonResponse({'code':0,'msg':'上传成功','data':{'src':aa}})

    except:
        return JsonResponse({'code':1,'msg':'上传失败'})

#商品展示图片上传视图
def upgoods_load(request):
    getfiles = request.FILES.getlist('file')
    try:
        if getfiles:
            aa = upgoods_pic_load(request)
            return JsonResponse({'code':0,'msg':'上传成功','data':{'src':aa}})
    except:
        return JsonResponse({'code':1,'msg':'上传失败'})

#商品详情上传图片
def upload_goods_con(request):

    getfile = request.FILES.get('file')

    # 得到源文件的后缀
    hz = getfile.name.split('.').pop()
    # 生成新的名称
    make_name = time.strftime("%Y%m%d", time.localtime()) +'.' + hz
    # 生成文件夹
    make_dir = './media/images/goods/content/' + str(time.time()).replace('.', '')+str(random.randrange(10000,99999))

    # if os.path.exists(make_dir):
    #     make_dir = make_dir
    # else:
    #     os.makedirs(make_dir)

    # 写入文件
    try:
        with open(make_dir + make_name, 'wb+') as pic:
            for p in getfile.chunks():
                pic.write(p)
    except:

        return False
    u_pic = make_dir + make_name
    return u_pic[1:]


#商品图片上传
def upgoods_pic_load(request):

    getfiles = request.FILES.getlist('file')
    pics = []
    for getfile in getfiles:

        #print(getfile)
        # 得到源文件的后缀
        hz = getfile.name.split('.').pop()
        # 生成新的名称
        make_name = time.strftime("%Y%m%d", time.localtime()) +'.' + hz
        # 生成文件夹

        make_dir = './media/images/goods/cache/' + str(time.time()).replace('.', '')+str(random.randrange(10000,99999))

        # if os.path.exists(make_dir):
        #     make_dir = make_dir
        # else:
        #     os.makedirs(make_dir)

        # 写入文件
        try:
            with open(make_dir + make_name, 'wb+') as pic:
                for p in getfile.chunks():
                    pic.write(p)
        except:

            return False

        u_pic = make_dir + make_name
        pics.append(u_pic[1:])


    return pics
    #return HttpResponse(9)








