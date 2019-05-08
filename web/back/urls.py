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
from django.contrib import admin
from . views import views,userviews,typeviews,goodsviews,brandviews,orderviews,authviews

urlpatterns = [
    #后台首页
    url(r'^$', views.back,name='back'),
#后台登录
    # 后台登录页
    url(r'^login.html$', views.back_login, name='back_login'),
    # 后台退出登录页
    url(r'^logout.html$', views.back_logout, name='back_logout'),

    #会员管理
    url(r'user/list.html$', userviews.userlist, name='userlist'),
    # 会员查看
    url(r'user/detail.html$', userviews.detail, name='detail'),
    # 审核会员
    url(r'user/changestatus$', userviews.changestatus, name='changestatus'),

#商品类别管理
    # 获取数据
    url(r'type/get_type_data.html$', typeviews.get_type_data, name='get_type_data'),
    #类别列表
    url(r'type/list.html$', typeviews.typelist, name='typelist'),
    #类别添加
    url(r'type/add.html$', typeviews.typeadd, name='typeadd'),
    #类别修改
    url(r'type/edit.html$', typeviews.typeedit, name='typeedit'),
    #类别删除
    url(r'type/del.html$', typeviews.typedel, name='typedel'),
    # 类别详情
    url(r'type/detail.html$', typeviews.typedetail, name='typedetail'),
    # 审核类别状态
    url(r'type/changestatus$', typeviews.type_change_status, name='type_change_status'),

#商品属性管理
    # 获取商品属性数据
    url(r'trait/gettype$', goodsviews.gettype, name='gettype'),
    # 商品特征
    url(r'trait/list.html$', goodsviews.goods_trait_list, name='goods_trait_list'),
    # 商品特征添加
    url(r'trait/add.html$', goodsviews.goods_trait_add, name='goods_trait_add'),
    # 商品特征修改
    url(r'trait/edit.html$', goodsviews.goods_trait_edit, name='goods_trait_edit'),


#商品管理
    # 获取商品数据
    url(r'goods/getgoods$', goodsviews.getgoods, name='getgoods'),
    #所有商品列表
    url(r'goods/list.html$', goodsviews.goodslist, name='goodslist'),
    #商品添加
    url(r'goods/add.html$', goodsviews.goodsadd, name='goodsadd'),
    #商品图片
    url(r'goods/picture.html$', goodsviews.goodspicture, name='goodspicture'),
    #商品编辑
    url(r'goods/edit.html$', goodsviews.goodsedit, name='goodsedit'),
    # 商品回收站
    url(r'goods/trash.html$', goodsviews.goodstrash, name='goodstrash'),
    #商品详情
    url(r'goods/detail.html$', goodsviews.goodsdetail, name='goodsdetail'),
    #修改状态
    url(r'goods/status$', goodsviews.goods_status, name='goods_status'),

    #商品详情图片上传
    url(r'goods/goodsupload.html$', goodsviews.goodsupload, name='goodsupload'),
    #商品图片上传
    url(r'goods/upgoods_load.html$', goodsviews.upgoods_load, name='upgoods_load'),
    #商品图片删除
    url(r'goods/pics_del.html$', goodsviews.pics_del, name='pics_del'),

#品牌管理
    # 获取商品数据
    url(r'brand/getdata$', brandviews.brand_getdata, name='brand_getdata'),
    # 品牌列表(已审核)
    url(r'brand/list.html$', brandviews.brand_list, name='brand_list'),
    # 添加品牌
    url(r'brand/add.html$', brandviews.brand_add, name='brand_add'),
    # 修改品牌
    url(r'brand/edit.html$', brandviews.brand_edit, name='brand_edit'),
    # 品牌详情
    url(r'brand/detail.html$', brandviews.brand_detail, name='brand_detail'),
    #品牌logo上传
    url(r'brand/upload$', brandviews.brand_upload, name='brand_upload'),
    # 品牌回收站
    url(r'brand/trash.html$', brandviews.brand_trash, name='brand_trash'),

#订单管理
    #获取订单数据
    url(r'order/getdata$', orderviews.order_getdata, name='order_getdata'),
    #获取订单详情数据
    url(r'order/detail/getdata$', orderviews.orderdetail_getdata, name='orderdetail_getdata'),

    #订单列表
    url(r'order/list.html$', orderviews.order_list, name='order_list'),
    #订单详情
    url(r'order/detail.html$', orderviews.order_detail, name='order_detail'),
    #订单状态修改
    url(r'order/edit.html$', orderviews.order_edit, name='order_edit'),

#权限管理auth_getdata
    # 回去管理员数据
    url(r'auth/getdata$', authviews.auth_getdata, name='auth_getdata'),
    #管理员列表
    url(r'auth/list.html$', authviews.auth_list, name='auth_list'),
    #管理员添加
    url(r'auth/add.html$', authviews.auth_add, name='auth_add'),
    #管理员头像添加
    url(r'auth/iconadd.html$', authviews.auto_user_icon, name='auto_user_icon'),
    #管理员名称检测
    url(r'auth/checkname.html$', authviews.auto_user_checkname, name='auto_user_checkname'),



]
