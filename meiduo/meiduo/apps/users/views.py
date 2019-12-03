# Create your views here.
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, constants
from .models import User


class UserRegisterView(CreateAPIView):
	"""
	path('users/', views.UserRegisterView.as_view()),
	用户注册
	"""
	serializer_class = serializers.CreateUserSerializer


class UserDetailView(RetrieveAPIView):
	"""
	用户详情
	"""
	serializer_class = serializers.UserDetailSerializer
	permission_classes = (IsAuthenticated,)

	def get_object(self):
		return self.request.user


# 用户名是否存在
class UsernameCountView(APIView):
	"""
	path('usernames/<str:username>/count/)', views.UsernameCountView.as_view()),
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
	path('mobiles/<int:mobile>/count/', views.MobileCountView.as_view()),
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


class AddressViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericAPIView):
	"""
	用户地址新增与修改
	"""
	serializer_class = serializers.UserAddressSerializer
	permissions = (IsAuthenticated,)

	def get_queryset(self):
		return self.request.user.addresses.filter(is_deleted=False)

	# GET /addresses/
	def list(self, request, *args, **kwargs):
		"""
		用户地址列表数据
		:param request:
		:param args:
		:param kwargs:
		:return:
		"""
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		user = self.request.user
		return Response({
			'user_id': user.id,
			'default_address_id': user.default_address_id,
			'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
			'addresses': serializer.data,
		})

	# POST /addresses/
	def create(self, request, *args, **kwargs):
		"""
		保存用户地址数据
		:param request:
		:param args:
		:param kwargs:
		:return:
		"""
		# 检查用户地址数据数据不能超过上限
		count = request.user.addresses.count()
		if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
			return Response({'message': '保存地址数据已达到上限'}, status=status.HTTP_400_BAD_REQUEST)

		return super(AddressViewSet, self).create(request, *args, **kwargs)

	# delete /addresses/<pk>/
	def destory(self, request, *args, **kwargs):
		"""
		处理删除
		:param request:
		:param args:
		:param kwargs:
		:return:
		"""
		address = self.get_object()

		# 进行逻辑删除
		address.is_deleted = True
		address.save()

		return Response(status=status.HTTP_204_NO_CONTENT)

	# put /addresses/pk/status/
	@action(method=['put'], detail=True)
	def status(self, request, pk=None):
		"""
		设置默认地址
		:param request:
		:param pk:
		:return:
		"""
		address = self.get_object()
		request.user.default_address = address
		request.user.save()
		return Response({'message': 'OK'}, status=status.HTTP_200_OK)

	# put /addresses/pk/title/
	# 需要请求体参数title
	@action(methods=['put'], detail=True)
	def title(self, request, pk=None):
		"""
		修改标题
		:param request:
		:param pk:
		:return:
		"""
		address = self.get_object()
		serializer = serializers.AddressTitleSerializer(instance=address, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)
