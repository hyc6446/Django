from django.urls import path
from . import views
urlpatterns = [
    path('index', views.index,name='index'),
    path('pc-geetest/register', views.pcgetcaptcha,name='pcgetcaptcha'),
    path('pc-geetest/validate', views.pcvalidate,name='pcvalidate'),
    path('pc-geetest/ajax_validate', views.pcajax_validate,name='pcajax_validate'),
    path('mobile-geetest/register', views.mobilegetcaptcha,name='mobilegetcaptcha'),
]
