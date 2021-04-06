from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserType, Book, Order, OrderBook

class UserTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserType
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  
  userTypeId = serializers.SerializerMethodField(read_only=True)
  isAdmin = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = User
    fields = ['id','userTypeId', 'username', 'email', 'first_name','last_name', 'isAdmin']

  def get_isAdmin(self, obj):
    return obj.is_staff

  def get_userTypeId(self, obj):
    librarian = 1
    user = 2
    if obj.is_staff:
      UserTypeId = librarian
    else:
      UserTypeId = user
    return UserTypeId

  def get_name(self, obj):
    name = obj.first_name
    if name == '':
      name = obj.email
    return name

class UserSerializerWithToken(UserSerializer):
  token = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'first_name','last_name', 'isAdmin', 'token']

  def get_token(self, obj):
    token = RefreshToken.for_user(obj)
    return str(token.access_token)


class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = '__all__'

  def get_available_book(self, obj):
    if obj.countInLibrary == 0:
      obj.isAvailable = False
      return obj.isAvailable

class OrderBookSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderBook
    fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
  orderBooks = serializers.SerializerMethodField(read_only=True)
  user = serializers.SerializerMethodField(read_only=True)

  class Meta:
    model = Order
    fields = '__all__'

  def get_orderBooks(self, obj):
    items = obj.orderbook_set.all()
    serializer = OrderBookSerializer(items, many=True)
    return serializer.data

  def get_user(self, obj):
    user = obj.user
    serializer = UserSerializer(user, many=False)
    return serializer.data
