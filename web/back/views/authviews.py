from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
# Create your views here.
from django.utils.html import format_html
from ..models import AuthUserInfo,JsonExtendEncoder
from django.contrib.auth.models import User
import datetime,time,json,random,shutil
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

#查询条件
def getKwargs(data={}):
   kwargs = {}
   for (k , v)  in data.items() :
       if v is not None :
           kwargs[k] = v
   return kwargs

#获取数据
def auth_getdata(request):
    #分页
    limit = int(request.GET.get('limit',20))
    page = int(request.GET.get('page',1))
    start = (page-1) * limit
    end = limit * page

    #获取品牌数据
    object = User.objects.all().order_by('-is_superuser')[start:end].values()
    print(object)
    for v in object:
        v['icon'] = AuthUserInfo.objects.get(user_id_id = v['id']).user_icon
    #转换Json格式
    obj = json.dumps(list(object), cls=JsonExtendEncoder, ensure_ascii=False)
    #拼接返回的数据
    datas={}
    datas['code']=0
    datas['msg'] = ''
    datas['count'] = User.objects.all().count()
    datas['data'] = json.loads(obj)
    return HttpResponse(json.dumps(datas))

#管理员列表
def auth_list(request):

    return render(request,'auth/user/list.html')

#管理员添加
def auth_add(request):
    if request.method == 'GET':
        return render(request,'auth/user/add.html')
    elif request.method == 'POST':
        try:
            data = getKwargs(request.POST)
            print(data)

            if data['is_superuser'] == '1':
                object = User.objects.create_superuser(data['username'],data['email'],data['password'])
            else:
                object = User.objects.create_user(data['username'],data['email'],data['password'])
            object.save()

            obj = AuthUserInfo()
            obj.user_icon = data['user_icon'].replace("/static/back/img/cache/", "/static/back/img/auth_user/")
            obj.user_id = object
            obj.save()
            shutil.move(settings.BASE_DIR + data['user_icon'], settings.BASE_DIR + '/static/back/img/auth_user/')

            return JsonResponse({'code':1,'msg':'添加成功'})
        except:
            return JsonResponse({'code':0,'msg':'添加失败'})
        #return HttpResponse(0)

#管理员名称检测
def auto_user_checkname(request):
    try:
        object = User.objects.get(username=request.GET.get('username'))
        if object:
            return JsonResponse({'code':1})
    except:
        return JsonResponse({'code':0})

#会员头像上传
def auto_user_icon(request):
    try:
        getfile = request.FILES.get('file')
        if getfile:
            path = auth_user_upload(request)
            if path:
                return JsonResponse({'code':1,'msg':'上传成功','path':path})
    except:
        return JsonResponse({'code':1,'msg':'上传成功'})


#上传头像
def auth_user_upload(request):

    getfile = request.FILES.get('file')

    # 得到源文件的后缀
    hz = getfile.name.split('.').pop()
    # 生成新的名称
    make_name = time.strftime("%Y%m%d", time.localtime()) + '.' + hz
    # 生成文件夹
    make_dir = './static/back/img/cache/' + str(time.time()).replace('.', '') + str(random.randrange(10000, 99999))

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










