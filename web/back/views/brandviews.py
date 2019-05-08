from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
# Create your views here.
from django.utils.html import format_html
from ..models import Brand,Types,JsonExtendEncoder

import datetime,time,json,random,shutil,os
from django.conf import settings
# Create your views here.

#查询条件
def getKwargs(data={}):
   kwargs = {}
   for (k , v)  in data.items() :
       if v is not None :
           kwargs[k] = v
   return kwargs

# 获取品牌数据
def brand_getdata(request):
    #分页
    limit = int(request.GET.get('limit',20))
    page = int(request.GET.get('page',1))
    start = (page-1) * limit
    end = limit * page

    #获取品牌数据
    object = Brand.objects.all().order_by('-b_name')[start:end]

    obj = list(object.values())
    for i in range(len(obj)):
        obj[i]['t_name'] = object[i].b_tid.first().t_name

    #转换Json格式
    obj = json.dumps(obj, cls=JsonExtendEncoder, ensure_ascii=False)
    #拼接返回的数据
    datas={}
    datas['code']=0
    datas['msg'] = ''
    datas['count'] = Brand.objects.all().count()
    datas['data'] = json.loads(obj)
    #print(datas)
    return HttpResponse(json.dumps(datas))

#查看、修改公用数据
def get_data(request):

    data = Brand.objects.get(id = request.GET.get('id'))
    data.t_id = data.b_tid.first().id
    types = Types.objects.filter(t_pid=0)
    context = {'data':data,'types':types}

    return context

# 品牌列表(已审核)
def brand_list(request):

    return render(request,'back/brand/list.html')


# 添加品牌
def brand_add(request):

    if request.method == 'GET':
        types = Types.objects.filter(t_pid = 0)

        return render(request,'back/brand/add.html',{'types':types})
    elif request.method == 'POST':
        try:
            data = getKwargs(request.POST)

            object= Brand()
            object.b_name = data['b_name']
            object.b_intro = data['b_intro']
            object.b_isdel = data['b_isdel']
            object.b_logo = data['b_logo'].replace("/media/images/cache/", "/media/images/brand/")
            shutil.move(settings.BASE_DIR + data['b_logo'], settings.BASE_DIR + '/media/images/brand/')
            object.save()
            object.b_tid.add(Types.objects.get(id=int(data['p_tid'])))

            return JsonResponse({'code':1,'msg':'品牌添加成功'})
        except:
            return JsonResponse({'code':0,'msg':'品牌添加失败'})
        #return HttpResponse(0)

#上传品牌logo
def brand_upload(request):
    getfile = request.FILES.get('file')
    try:
        if getfile:
            path = brand_logo_upload(request)
            return JsonResponse({'code':1,'msg':'上传成功','path':path})
    except:
        return JsonResponse({'code':0,'msg':'上传失败'})


# 品牌回收站
def brand_trash(request):


    return render(request)

# 品牌信息修改
def brand_edit(request):
    if request.method == 'GET':

        data = get_data(request)
        return render(request,'back/brand/edit.html',data)
    elif request.method == 'POST':
        try:
            data = getKwargs(request.POST)
            object = Brand.objects.get(id = int(data['id']))
            old_path = object.b_logo
            object.b_name = data['b_name']
            object.b_intro = data['b_intro']
            object.b_isdel = data['b_isdel']
            if data['b_logo']:
                #修改保存到数据库的图片地址
                object.b_logo = data['b_logo'].replace("/media/images/cache/", "/media/images/brand/")
                shutil.move(settings.BASE_DIR + data['b_logo'], settings.BASE_DIR + '/media/images/brand/')
                if os.path.exists(settings.BASE_DIR +str(old_path)):
                    os.remove(settings.BASE_DIR +str(old_path))
            object.b_tid.clear()
            object.b_tid.add(Types.objects.get(id=int(data['p_tid'])))

            object.save()
            return JsonResponse({'code':1,'msg':'修改成功'})
        except:
            return JsonResponse({'code':0,'msg':'修改失败'})



# 品牌信息查看
def brand_detail(request):

    data = get_data(request)

    return render(request,'back/brand/detail.html',data)

#上传logo
def brand_logo_upload(request):

    getfile = request.FILES.get('file')

    # 得到源文件的后缀
    hz = getfile.name.split('.').pop()
    # 生成新的名称
    make_name = time.strftime("%Y%m%d", time.localtime()) + '.' + hz
    # 生成文件夹
    make_dir = './media/images/cache/' + str(time.time()).replace('.', '') + str(
        random.randrange(10000, 99999))

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