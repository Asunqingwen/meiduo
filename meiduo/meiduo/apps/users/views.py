# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo.apps.users.models import User
from .serializers import CreateUserSerializer


class UserRegisterView(CreateAPIView):
	"""
	re_path(r'^users/register$', views.UserRegisterView.as_view()),
	用户注册
	"""
	serializer_class = CreateUserSerializer


# 用户名是否存在
class CheckUsernameView(APIView):
	"""
	re_path(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
	用户名数量
	"""

	def get(self, request, username):
		"""
		获取指定用户名数量
		:param request:
		:param username:
		:return:
		"""
		count = User.objects.filter(username=username).count()

		data = {
			'username': username,
			'count': count,
		}
		return Response(data)


# 手机号是否存在
class MobileCountView(APIView):
	"""
	re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
	手机号数量
	"""

	def get(self, request, mobile):
		"""
		获取指定手机号数量
		:param request:
		:param mobile:
		:return:
		"""
		count = User.objects.filter(mobile=mobile).count()

		data = {
			'mobile': mobile,
			'count': count,
		}
		return Response(data)
