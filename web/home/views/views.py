from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password, check_password
from back.models import Users,Types,Goods,Pictures,GoodsInfo,Address,Orders,OrderDetail

from decimal import *
import random,os,time
from django.db.models import Q
# Create your views here.

#查询条件
def getKwargs(data={}):
   kwargs = {}
   for (k , v)  in data.items() :
       if v is not None :
           kwargs[k] = v
   return kwargs

#查询分类导航数据
def get_types_data(request):

    data = Types.objects.filter(t_pid=0)
    for object in data:
        object.sub = Types.objects.filter(t_pid = object.id)
        for obj in object.sub:
            obj.tsub = Types.objects.filter(t_pid = obj.id)

    return data

#首页
def index(request):

    data = get_types_data(request)
    print(data)
    return render(request, 'home/index.html',{'type':data})

#商品列表
def list(request,tid):
    #查询导航分类数据
    nav_types = get_types_data(request)
    # try:
    #分类产品数据
    datas = {}

    types = Types.objects.filter(t_pid = tid)
    if types:
        for type in types:
            data = Goods.objects.filter(g_tid_id = type.id).order_by('g_addtime')
    else:
        data = Goods.objects.filter(g_tid = tid).order_by('g_addtime')
        for p in data:
            p.pic =  Pictures.objects.filter(p_gid_id=p.id).filter(p_cover = 1)
    # except:
    #     datas = Goods.objects.all().order_by('g_addtime')

    datas['tname'] = Types.objects.get(id = tid).t_name
    datas['counts'] = types.count()
    datas['data'] = data

    #获取产品品牌


    return render(request,'home/list.html',{'data':datas,'type':nav_types})

#商品详情
def content(request,tid):

    #查询导航分类数据
    nav_types = get_types_data(request)
    #查询商品信息
    data=Goods.objects.get(id = tid)
    goodpics = Pictures.objects.filter(p_gid = tid)
    goodinfo = GoodsInfo.objects.get(i_gid = tid)

    #查询当前路径
    currpath = {}
    pid = Types.objects.get(id = data.g_tid_id).t_pid
    find_tid = Types.objects.filter(t_pid = pid)
    if find_tid:
        currpath['main'] = Types.objects.get(id = pid)
        currpath['sub'] = Types.objects.get(id = data.g_tid_id)
    else:
        currpath={}

    #查同类产品
    like_goods = Goods.objects.filter(g_tid=data.g_tid_id).exclude(id = tid).order_by('-g_sellnum')[:6]

    context = {'data':data,'goodpics':goodpics,'goodinfo':goodinfo,'type':nav_types,'currpath':currpath,'like_goods':like_goods}
    return render(request,'home/content.html',context)

#搜索页面
def search(request):

    return render(request,'home/index.html')
#会员登录
def login(request):

    if request.method == 'GET':
        return render(request,'home/login.html')
    elif request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        # try:
        res = Users.objects.get(username=uname)
        if res:
            depwd = check_password(pwd, res.password)
            if depwd:
                request.session['vipuser'] = {'id': res.id, 'username': res.username}
                # return HttpResponseRedirect(reverse('index'))
                return JsonResponse({'code': 1})
        #     return JsonResponse({'code': 0})
        # except:
        #     return JsonResponse({'code': -1})

        return HttpResponse(0)
#会员退出
def loginout(request):

    del request.session['vipuser']

    return HttpResponseRedirect(reverse('login'))

#会员注册
def register(request):
    if request.method == 'GET':

        return render(request,'home/register.html')
    elif request.method == 'POST':
        try:
            object = Users()
            object.username = request.POST.get('username')
            object.u_phone = request.POST.get('phone')
            object.password = make_password(request.POST.get('password'), None, 'pbkdf2_sha256')
            object.save()
            request.session['vipuser']={'username':object.username,'level':object.u_level.l_name,'id':object.id}
            return render(request,'home/msg.html',{'msg':'恭喜你注册成功!现在开启购物之旅,祝您购物愉快！'})

        except:
            return render(request,'home/index.html')
        #return HttpResponse(0)

#会员注册检测用户名
def checkusername(request):
    val = request.GET.get('username')

    try:
        res= Users.objects.filter(username__contains=val)
        if res[0]:
            return JsonResponse({"rel": 1})
        else:
            return JsonResponse({"rel": 0})
    except:
        return JsonResponse({'code':-1})
    #return HttpResponse(00)

#重置密码
def resetpwd(request):

    return render(request,'home/index.html')

def forgotpwd(request):

    return render(request,'home/forgot-pwd.html')

#购物车添加
def cart_add(request):
    try:
        gid = request.GET.get('gid')
        num = int(request.GET.get('num'))
        data = Goods.objects.get(id = gid)
        pic = data.pictures_set.filter(p_cover=1)[0]
        cart = request.session.get('cart',{})
        if gid in cart.keys():
            cart[gid]['num'] = num
        else:
            cart[gid] = {'id':data.id,'name':data.g_name,'price':float(data.g_price),'pic':str(pic.p_pic),'num':num,'color':data.goodsinfo.i_color}

        request.session['cart'] = cart
        return JsonResponse({'code':1,'msg':'添加购物车成功','num':cart[gid]['num']})
    except:
        return JsonResponse({'code':0,'msg':'添加购物车失败'})
    #return HttpResponse(0)

# 购物车列表
def cart_list(request):
    data = request.session.get('cart',{})

    return render(request,'home/cart.html',{'data':data})

#清空购物车
def cart_clear(request):
    try:
        request.session['cart']={}
        return JsonResponse({'code':1,'msg':'购物车清空成功'})
    except:
        return JsonResponse({'code':0,'msg':'购物车清空失败'})

#清除购物车中的数据
def cart_delete(request):
    try:
        gid = request.GET.get('gid')
        data = request.session['cart']
        del request.session['cart'][gid]
        request.session['cart'] = data
        return JsonResponse({'code':1,'msg':'删除成功'})
    except:
        return JsonResponse({'code':0,'msg':'删除失败'})

#购物车结算
def cart_order(request):
    try:
        getgoods = eval(request.POST.get('checked_goods'))
        data={}
        for v in getgoods:
            obj = Goods.objects.get(id = v['gid'])
            pic = obj.pictures_set.filter(p_cover=1)[0]
            v['id'] = obj.id
            v['color'] = obj.goodsinfo.i_color
            v['name'] = obj.g_name
            v['price'] = float(obj.g_price)
            v['pic'] = str(pic.p_pic)
            v['num'] = int(v['num'])
        data['items'] = getgoods

        request.session['cart_select'] = data
        address = Address.objects.filter(u_uid = request.session['vipuser']['id'])

        return render(request,'home/confirm-order.html',{'data':data, 'address':address})
    except:
        return HttpResponseRedirect(reverse('cart_list'))

#购物车生成订单
def make_order(request):
    try:
        data = request.session['cart_select']
        totalNum = 0
        totalPrice = 0
        for val in data.values():
            for vv in val:
                totalNum += int(vv['num'])
                totalPrice += float(vv['price']) * int(vv['num'])
        adobj = Address.objects.get(id=request.POST.get('aid'))
        object = Orders()
        object.o_number = makenumber(request)
        object.o_totalprice = totalPrice
        object.o_totalnum = totalNum
        object.o_uid = Users.objects.get(id=request.session['vipuser']['id'])
        object.o_address = adobj

        object.save()
        for val in data.values():
            for v in val:
                # 生成订单详情
                gobj = Goods.objects.get(id=v['gid'])
                obj = OrderDetail()
                obj.d_pic = v['pic']
                obj.d_num = v['num']
                obj.d_oid = object
                obj.d_gid = gobj
                obj.save()

                # 修改商品库存数量
                gobj.g_sellnum += int(v['num'])
                gobj.g_invnum = gobj.g_nums - gobj.g_sellnum
                gobj.save()

                # 清空提交的订单session
                request.session['cart_select'] = {}

        return HttpResponseRedirect('pay/order.html?orderid='+str(object.id))
    except:
        return HttpResponseRedirect(reverse('cart_list'))
    #return HttpResponse(0)


#支付页面
def cart_pay(request):
    orderid = request.GET.get('orderid')

    data = Orders.objects.get(id = orderid)
    details  = data.orderdetail_set.all()
    goods = []
    for v in details:
        obj = Goods.objects.get(id = v.d_gid_id)
        goods.append({'name':obj.g_name,'num':v.d_num})
    address = Address.objects.get(id = data.o_address_id)
    return render(request,'home/pay.html',{'data':data,'goods':goods,'address':address})

#支付成功
def pay_success(request):

    return render(request,'home/success.html')

#添加收货地址
def add_address(request):
    try:
        data = getKwargs(request.GET)
        data['u_address'] = data['provid']+','+data['cityid']+','+data['areaid']
        data['u_uid'] = Users.objects.get(id = request.session['vipuser']['id'])
        object = Address()
        object.u_name = data['u_name']
        object.u_iphone = data['u_iphone']
        object.u_fixphone = data['u_fixphone']
        object.u_address = data['u_address']
        object.u_detail = data['u_detail']
        object.u_uid = data['u_uid']
        object.u_status = 0
        object.save()
        return JsonResponse({'code':1,'msg':'添加成功'})
    except:
        return JsonResponse({'code':0,'msg':'添加失败'})

    # return HttpResponse(0)

#设置默认收货地址
def set_address(request):
    try:
        for i in Address.objects.filter(u_uid = request.session['vipuser']['id']):
            i.u_status = 0
            i.save()
        object = Address.objects.get(id = request.GET.get('sid'))
        object.u_status = 1
        object.save()
        return JsonResponse({'code':1,'msg':'设置默认地址成功'})
    except:
        return JsonResponse({'code':0,'msg':'设置默认地址失败'})



#====================================会员中心===================
#会员中心
def member(request):

    data = Users.objects.get(id = request.session['vipuser']['id'])

    return render(request,'home/uc.html',{'data':data})

#个人头像
def uc_buddha(request):
    #获取前台传输的文件
    getfile = request.FILES.get('file')
    id = request.POST.get('id')

    #得到当前对象
    object = Users.objects.get(id=id)

    try :
        picpath = upload(request)
        #判断是否是默认头像
        if getfile == '/static/default/time.jpg':
            object.u_pic = '/static/default/time.jpg'
        else:

            object.u_pic = picpath
        #保存修改
        object.save()
        return JsonResponse({"code": 0, "msg": "上传成功", "data": {"src": picpath}})
    except:
        return JsonResponse({"code": 1, "msg": "上传失败", "data": {"src": picpath}})

#个人信息
def uc_account(request):

    if request.method == 'GET':         #个人信息页面
        data = Users.objects.get(id=request.session['vipuser']['id'])
        return render(request,'home/uc-account.html',{'data':data})
    elif request.method == 'POST':      #修改会员信息
        try:
            id = request.POST.get('uid')
            object = Users.objects.get(id=id)

            if request.POST.get('province'):
                addpath = request.POST.get('province','') + ',' + request.POST.get('city','') + ',' + request.POST.get('area','')
            else:
                addpath=''
            object.truename = request.POST.get('truename')
            object.sex = request.POST.get('sex')
            object.age = request.POST.get('age')
            object.u_phone = request.POST.get('phone')
            object.u_address = addpath
            object.u_intro = request.POST.get('intro')
            object.save()

            return JsonResponse({'code':1})
        except:

            return JsonResponse({'code':0})
        # return HttpResponse(0)


#收货地址
def uc_address(request):

    return render(request,'home/uc-address.html')

#我的订单
def uc_myorder(request):
    data = Orders.objects.filter(o_uid= request.session['vipuser']['id'])
    print(data)
    return render(request,'home/uc-order.html',{'data':data})

#订单详情
def uc_order_detail(request):

    return render(request,'home/uc-order-detail.html')

#商品评价
def uc_evaluate(request):

    return render(request,'home/uc-evaluate.html')





#==================================其他功能=================================================

#信息提示
def msg(request):

    return render(request,'home/msg.html',{'msg':'默认提示'})

#生成订单号
def makenumber(request):
    number = str(time.time()).replace('.','')[:10]+str(random.randrange(0000,9999))

    return int(number)

#上传会员头像
def upload(request):
    #获取前台传输的文件
    getfile = request.FILES.get('file')
    id = request.POST.get('id')
    #得到源文件的后缀
    hz = getfile.name.split('.').pop()
    #生成新的名称
    make_name = time.strftime("%Y%m%d", time.localtime())+'_'+id+'.'+hz
    #生成文件夹
    make_dir = './media/images/user/'+time.strftime("%Y%m%d", time.localtime())+'/'
    print(make_dir)
    if os.path.exists(make_dir):
        make_dir = make_dir
    else:
        os.makedirs(make_dir)
    #写入文件
    try:
        with open(make_dir+make_name, 'wb+') as pic:
            for p in getfile.chunks():
                pic.write(p)
    except:
        return False
    u_pic = make_dir+make_name
    return u_pic[1:]







