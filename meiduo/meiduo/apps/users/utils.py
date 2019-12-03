# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 0002 10:20
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: utils.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
import re

from django.contrib.auth.backends import ModelBackend

from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
	"""
	自定义jwt认证成功后的返回数据
	:param token:
	:param user:
	:param request:
	:return:
	"""
	return {
		'token': token,
		'user_id': user.id,
		'username': user.username,
	}


def get_user_by_account(account):
	"""
	根据账号获取user对象
	:param account: 账号，可以是用户名，也可以是手机
	:return: User对象 或者 None
	"""
	try:
		if re.match('^1[3-9]\d{9}$', account):
			# 账号为手机号
			user = User.objects.get(mobile=account)
		else:
			# 账号为用户名
			user = User.objects.get(username=account)
	except User.DoesNotExist:
		return None
	else:
		return user


class UsernameMobileAuthBackend(ModelBackend):
	"""
	自定义手机号码或用户名认证
	"""

	def authenticate(self, request, username=None, password=None, **kwargs):
		user = get_user_by_account(username)
		if not user and user.check_password(password):
			return user
