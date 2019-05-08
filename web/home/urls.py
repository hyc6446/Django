"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
from .views import views

urlpatterns = [

    #获取分类导航数据
    url(r'type/nav.html$', views.get_types_data, name='get_types_data'),
    #商品列表页
    url(r'list/(?P<tid>[0-9]+).html$', views.list, name='list'),
    #商品内容页
    url(r'content/(?P<tid>[0-9]+).html$', views.content, name='content'),
    #搜索页面
    url(r'search.html$', views.search, name='search'),
    #登录页面
    url(r'login.html$', views.login, name='login'),
    # 退出登录页面
    url(r'loginout$', views.loginout, name='loginout'),
    # 注册页面
    url(r'register.html$', views.register, name='register'),
    #用户名检测
    url(r'checkusername$', views.checkusername, name='checkusername'),
    #重置密码
    url(r'resetpwd.html$', views.resetpwd, name='resetpwd'),
    # 忘记密码
    url(r'forgotpwd.html$', views.forgotpwd, name='forgotpwd'),

    # 信息提示
    url(r'msg.html$', views.msg, name='msg'),

#会员模块

    #会员中心
    url(r'uc/uc.html$', views.member, name='member'),
    #个人信息
    url(r'uc/account.html$', views.uc_account, name='uc_account'),
    #个人头像
    url(r'uc/buddha.html$', views.uc_buddha, name='uc_buddha'),
    #收货地址
    url(r'uc/address.html$', views.uc_address, name='uc_address'),


    #我的订单
    url(r'uc/myorder.html$', views.uc_myorder, name='uc_myorder'),
    #订单详情
    url(r'uc/order/detail.html$', views.uc_order_detail, name='uc_order_detail'),
    #商品评价
    url(r'uc/evaluate.html$', views.uc_evaluate, name='uc_evaluate'),

#购物车
    #添加购物车
    url(r'add/cart.html$', views.cart_add, name='cart_add'),
    #购物车列表
    url(r'list/cart.html$', views.cart_list, name='cart_list'),
    #购物车订单列表
    url(r'cart/order.html$', views.cart_order, name='cart_order'),
    # 添加收货地址
    url(r'cart/add_address.html$', views.add_address, name='add_address'),
    # 设置收货地址
    url(r'cart/set_address.html$', views.set_address, name='set_address'),
    # 购物车生成订单
    url(r'pay/make/order.html$', views.make_order, name='make_order'),
    #购物车结算
    url(r'pay/order.html$', views.cart_pay, name='cart_pay'),
    # 结算成功
    url(r'pay/success.html$', views.pay_success, name='pay_success'),

    #购物车清空
    url(r'cart/clear.html$', views.cart_clear, name='cart_clear'),
   #购物车删除
    url(r'cart/delete.html$', views.cart_delete, name='cart_delete'),



#其他功能模块

    #文件上传
    url(r'upload/$', views.upload, name='upload'),

    # 首页
    url(r'^$', views.index, name='index'),


]

