from django import template
from django.utils.html import format_html
register = template.Library()

#注册标签
# #手机号码的加密
@register.simple_tag
def SetPhone(phone):

    phone = str(phone)
    newphone = phone[:3]+'****'+phone[7:]
    return newphone

#计算金额
@register.simple_tag
def salaprice(price,num):

    total = float(price) * int(num)
    return total



