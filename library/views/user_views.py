from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from library.serializers import UserTypeSerializer, UserSerializer, UserSerializerWithToken
from library.models import UserType, User
from rest_framework import status
from rest_framework.response import Response

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
    data = super().validate(attrs)
    serializer = UserSerializerWithToken(self.user).data
    for k, v in serializer.items():
      data[k] = v
    return data

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUserType(request):
  data = request.data
  print(data)
  try:
    User_type = UserType.objects.create(
      name=data['name'],
      isActive=data['isActive'],
    )
    serializer = UserTypeSerializer(User_type, many=False)
    return Response(serializer.data)
  except:
    message = {'detail': 'User type with this name already exists'}
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
      user = User.objects.create(
        first_name=data['first_name'],
        last_name = data['last_name'],
        username=data['email'],
        email=data['email'],
        is_staff = data['isAdmin'],
        password=make_password(data['password'])
      )
      serializer = UserSerializerWithToken(user, many=False)
      return Response(serializer.data)
    except:
      message = {'detail': 'User with this email already exists'}
      return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
  user = request.user
  serializer = UserSerializer(user, many=False)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
  user = User.objects.get(id=pk)
  serializer = UserSerializer(user, many=False)
  return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
  user = User.objects.get(id=pk)
  data = request.data
  user.first_name = data['first_name']
  user.last_name = data['last_name']
  user.username = data['email']
  user.email = data['email']
  user.is_staff = data['isAdmin']
  user.save()
  serializer = UserSerializer(user, many=False)
  return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUserType(request, pk):
  User_type = UserType.objects.get(id=pk)
  data = request.data
  User_type.name = data['name']
  User_type.isActive = data['isActive']
  User_type.save()
  serializer = UserTypeSerializer(
    User_type, many=False)
  return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
  userForDeletion = User.objects.get(id=pk)
  userForDeletion.delete()
  return Response('User was deleted')
