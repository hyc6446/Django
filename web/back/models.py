from django.db import models
from django.contrib.auth.models import User
import json
from datetime import date
from datetime import datetime
# Create your models here.


#===================网站后端模型========================
#管理员表
class AuthUserInfo(models.Model):

    user_id = models.OneToOneField(User,unique=True,verbose_name=('用户id'))
    user_icon = models.CharField(max_length=100,default='/static/default/timg.jpg')

    class Meta:
        db_table = 'auth_user_info'


#===================网站前端模型========================
#网站会员模型
class Users(models.Model):
    #用户名
    username = models.CharField(max_length=30,null=False,verbose_name='用户名')
    #登录密码
    password = models.CharField(max_length=80,null=False,verbose_name='登录密码')
    #真实姓名
    truename = models.CharField(max_length=20,default='',verbose_name='真实姓名')
    #性别
    sex = models.CharField(max_length=1,default='男',verbose_name='性别')
    #年龄
    age = models.IntegerField(default=18,verbose_name='年龄')
    #地址
    u_address = models.CharField(max_length=100,default='',verbose_name='地址')
    #手机号
    u_phone = models.CharField(max_length=11,default='',verbose_name='手机号')
    #邮箱
    u_email = models.CharField(max_length=30,default='',verbose_name='邮箱')
    #用户头像
    u_pic = models.FileField(max_length=100,upload_to='images/user/',default='/static/default/timg.jpg',verbose_name='用户头像')
    #用户等级
    u_level = models.ForeignKey(to='UserLevel',to_field='id',default=1,verbose_name='用户等级')
    #用户状态
    u_status = models.CharField(max_length=10,default='未审核',verbose_name='用户状态')
    #用户介绍
    u_intro = models.TextField(default='这家伙很懒',verbose_name='用户介绍')
    #注册时间
    u_addtime = models.DateTimeField(auto_now_add=True,verbose_name='注册时间')

    class Meta:
        db_table = 'mall_users'

        permissions = (
            ("show_user", "会员模块查看权限"),
            ("edit_user", "会员模块修改权限"),
            ("insert_user",  "会员模块增加权限"),
            ("del_user",  "会员模块删除权限"),
        )


#会员等级表
class UserLevel(models.Model):
    #等级名称
    l_name = models.CharField(max_length=5)
    class Meta:
        db_table = 'mall_user_level'


#商品类别表
class Types(models.Model):
    t_name = models.CharField(max_length=30,null=False,verbose_name='类别名称')
    t_pid = models.IntegerField(default=0,null=False,verbose_name='父级栏目id')
    t_path = models.CharField(max_length=30,default='',verbose_name='类别路径')
    t_info = models.CharField(max_length=50,verbose_name='栏目简介')
    t_icon = models.CharField(max_length=50,default='fa-black-tie',verbose_name='栏目图标')
    t_isdel = models.IntegerField(default=1,verbose_name='是否删除') # 0:删除状态  1：正常状态
    t_addtime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    t_altertime = models.DateTimeField(auto_now=True,verbose_name='最后修改时间')

    class Meta:
        db_table = 'mall_types'

        permissions = (
            ("show_types", "商品类别模块查看权限"),
            ("edit_types", "商品类别模块修改权限"),
            ("insert_types",  "商品类别模块增加权限"),
            ("del_types",  "商品类别模块删除权限"),
        )


#商品特征信息表
class GoodsAttr(models.Model):
    a_name = models.CharField(max_length=30,verbose_name='商品特征名称')
    a_pid = models.IntegerField(default=0,verbose_name='父级id')
    a_info = models.CharField(max_length=50,default='暂无简介',verbose_name='特征简介')
    a_isdel = models.IntegerField(default=1,verbose_name='特征状态')  #1:使用状态 0 ：禁用状态
    a_path = models.CharField(max_length=30,default='',verbose_name='所属父类路径')
    a_addtime = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    a_altertime = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    class Meta:
        db_table = 'mall_goodsattr'
        permissions = (
            ("show_attr", "商品属性模块查看权限"),
            ("edit_attr", "商品属性模块修改权限"),
            ("insert_attr", "商品属性模块增加权限"),
            ("del_attr", "商品属性模块删除权限"),
        )

#商品表
class Goods(models.Model):
    g_name = models.CharField(max_length=255,null=False,verbose_name='商品名称')
    g_title = models.CharField(max_length=255,verbose_name='简短介绍')
    g_price = models.DecimalField(max_digits = 10,decimal_places = 2,null=False,verbose_name='商品价格')
    g_saleprice = models.DecimalField(max_digits = 3,decimal_places = 2,default=0,verbose_name='商品折扣')
    g_address = models.CharField(max_length=255,default='',verbose_name='商品产地')
    g_type = models.IntegerField(default=0,verbose_name='商品所属类别')  #0:普通  1：新品  2：热卖
    g_mall =models.CharField(max_length=4,default='',verbose_name='是否包邮') #0:不包邮  1：包邮
    g_tid = models.ForeignKey(to='Types',to_field='id',verbose_name='商品类别')
    g_nums = models.IntegerField(default=0,verbose_name='商品数量')
    g_invnum = models.IntegerField(default=0,verbose_name='商品库存')
    g_sellnum = models.IntegerField(default=0,verbose_name='商品售卖数量')
    g_isdel = models.IntegerField(default=1,verbose_name='商品状态')  #1:为显示  0：不显示
    g_intro = models.CharField(max_length=255,verbose_name='商品简介')
    g_addtime = models.DateTimeField(auto_now_add=True,verbose_name='商品添加时间')
    g_altertime = models.DateTimeField(auto_now=True,verbose_name='商品修改时间')

    class Meta:
        db_table = 'mall_goods'
        permissions = (
            ("show_goods", "商品模块查看权限"),
            ("edit_goods", "商品模块修改权限"),
            ("insert_goods", "商品模块增加权限"),
            ("del_goods", "商品模块删除权限"),
        )
#商品信息表
class GoodsInfo(models.Model):
    i_gid = models.OneToOneField(Goods,on_delete=models.CASCADE)
    i_info = models.TextField(default='暂无商品详情',verbose_name='商品详情')
    i_color = models.CharField(max_length=30,default='',verbose_name='商品颜色')
    i_size = models.CharField(max_length=30,default='',verbose_name='商品尺寸')
    i_pinpai = models.CharField(max_length=30,default='',verbose_name='商品品牌')
    i_hot = models.IntegerField(default=0,verbose_name='')
    class Meta:
        db_table = 'mall_goodsinfo'
        permissions = (
            ("show_goodsinfo", "商品信息查看权限"),
            ("edit_goodsinfo", "商品信息修改权限"),
            ("insert_goodsinfo", "商品信息增加权限"),
            ("del_goodsinfo", "商品信息删除权限"),
        )
#商品图片表
class Pictures(models.Model):
    p_name = models.CharField(max_length=255,verbose_name='图片名称')
    p_pic = models.ImageField(max_length=255,upload_to='images/goods/',default='/static/default/timg.jpg',verbose_name='商品图片')
    p_gid = models.ForeignKey(to='Goods',to_field='id',verbose_name='图片所属商品id')
    p_sort = models.IntegerField(default=0,verbose_name='图片排序标示')
    p_cover = models.IntegerField(default=0,verbose_name='封面图面标示')  #0：普通图片  1：主图
    p_isdel = models.IntegerField(default=1,verbose_name='图片是否前台显示')
    p_addtime = models.DateTimeField(auto_now_add=True,verbose_name='图片添加时间')
    p_altertime = models.DateTimeField(auto_now=True,verbose_name='图片修改时间')

    class Meta:
        db_table = 'mall_pictures'
        permissions = (
            ("show_goodspic", "商品图片查看权限"),
            ("edit_goodspic", "商品图片修改权限"),
            ("insert_goodspic", "商品图片增加权限"),
            ("del_goodspic", "商品图片删除权限"),
        )
#商品品牌
class Brand(models.Model):
    b_name = models.CharField(max_length=50,verbose_name='品牌名称')
    b_logo = models.ImageField(max_length=100,upload_to='images/brand/',default='/static/default/timg.jpg',verbose_name='品牌logo')
    b_intro = models.TextField(max_length=255,verbose_name='品牌简介')
    b_tid = models.ManyToManyField(to="Types")
    b_isdel = models.CharField(max_length=4,default='启用',verbose_name='品牌简介') # 0:未启用 1：已启用
    b_addtime = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    b_altertime = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    class Meta:
        db_table = 'mall_brand'

        permissions = (
            ("show_brand", "品牌查看权限"),
            ("edit_brand", "品牌修改权限"),
            ("insert_brand", "品牌增加权限"),
            ("del_brand", "品牌删除权限"),
        )
#会员收货地址
class Address(models.Model):
    u_uid = models.ForeignKey(to='Users',to_field='id',verbose_name='会员id')
    u_name = models.CharField(max_length=50,verbose_name='收货人名称')
    u_iphone = models.CharField(max_length=12,verbose_name='收货人手机')
    u_fixphone = models.CharField(max_length=10,verbose_name="固定电话")
    u_address = models.CharField(max_length=255,verbose_name='收货地址')
    u_detail = models.CharField(max_length=100,verbose_name='地址详细')
    u_postcode = models.CharField(max_length=7,verbose_name='邮编')
    u_status = models.IntegerField(default=0,verbose_name='默认地址')   # 0 :取消默认 1：设为默认
    u_addtime = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    u_altertime = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    class Meta:
        db_table = 'mall_user_address'
        permissions = (
            ("show_goodspic", "商品图片查看权限"),
            ("edit_goodspic", "商品图片修改权限"),
            ("insert_goodspic", "商品图片增加权限"),
            ("del_goodspic", "商品图片删除权限"),
        )
#会员订单
class Orders(models.Model):
    o_number = models.CharField(max_length=20,verbose_name='订单编号') #组合:商品父id+商品id+订单生成时间戳+3位随机数
    o_totalprice = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='订单总价')
    o_totalnum = models.IntegerField(default=0,verbose_name='订单商品总数量')
    o_address = models.ForeignKey(to='Address',to_field='id',verbose_name='订单收货地址')
    o_status = models.IntegerField(default=1,verbose_name='订单状态') # 0:订单取消，1：下单未付款，2.付款未发货，3.已发货，位签收，4.订单完成
    o_addtime = models.DateTimeField(auto_now_add=True,verbose_name='生成时间')
    o_uid = models.ForeignKey(to='Users',to_field='id',verbose_name='用户id')
    class Meta:
        db_table = 'mall_orders'
        permissions = (
            ("show_order", "订单查看权限"),
            ("edit_order", "订单修改权限"),
            ("insert_order", "订单增加权限"),
            ("del_order", "订单删除权限"),
        )
#订单详情
class OrderDetail(models.Model):
    d_gid = models.ForeignKey(to='Goods',to_field='id',verbose_name='商品id')
    d_oid = models.ForeignKey(to='Orders',to_field='id',verbose_name='订单id')
    d_pic = models.CharField(max_length=100,verbose_name='商品图片')
    d_num = models.IntegerField(default=0,verbose_name='购买的商品数量')

    class Meta:
        db_table = 'mall_order_detail'

#商品评论
# class reviews(models.Model):
#     r_gid =





    #数据转json格式
class JsonExtendEncoder(json.JSONEncoder):
    """
        This class provide an extension to json serialization for datetime/date.
    """
    def default(self, o):
        """
            provide a interface for datetime/date
        """
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)

if __name__ == '__main__':
    d = {'now': datetime.now(), 'today': date.today(), 'i': 100}
    ds = json.dumps(d, cls=JsonExtendEncoder)
    print("ds type:", type(ds), "ds:", ds  )
    l = json.loads(ds)
    print( "l  type:", type(l), "ds:", l )


