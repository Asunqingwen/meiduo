# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 0002 10:08
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: urls.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views

router = routers.DefaultRouter()
router.register(r'address', views.AddressViewSet, base_name='addresses')

urlpatterns = [
	path('users/', views.UserRegisterView.as_view()),
	path('usernames/<str:username>/count/)', views.UsernameCountView.as_view()),
	path('mobiles/<int:mobile>/count/', views.MobileCountView.as_view()),
	path('authorizations/', obtain_jwt_token),  # 登录认证
]
urlpatterns += router.urls
