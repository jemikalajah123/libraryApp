from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from library.models import Book, Order, OrderBook
from library.serializers import BookSerializer, OrderSerializer
from rest_framework import status
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderBooks(request):
  user = request.user
  data = request.data
  OrderBooks = data['OrderBooks']
  print(len(OrderBooks))
  if OrderBooks and len(OrderBooks) == 0:
    return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
  else:
    # (1) Create order
    order = Order.objects.create(
      user=user,
      returnDate=data['returnDate'], 
    )
    # (2) Create order items adn set order to OrderBook relationship
    for i in OrderBooks:
      print(i['book'])
      book = Book.objects.get(id=i['book'])
      item = OrderBook.objects.create(
        book=book,
        order=order,
      )
    serializer = OrderSerializer(order, many=False)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
  user = request.user
  orders = user.order_set.all()
  serializer = OrderSerializer(orders, many=True)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
  orders = Order.objects.all()
  serializer = OrderSerializer(orders, many=True)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
  user = request.user
  try:
    order = Order.objects.get(id=pk)
    if user.is_staff or order.user == user:
      serializer = OrderSerializer(order, many=False)
      return Response(serializer.data)
    else:
      Response({'detail': 'Not authorized to view this order'},
      status=status.HTTP_400_BAD_REQUEST)
  except:
    return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateReturnBook(request, pk):
  order = Order.objects.get(id=pk)
  if order.orderState == "Approved":
    order.status = "Returned"
    order.save()
    orderBooks = OrderBook.objects.filter(order=order.id)
    for orderBook in orderBooks:
      books = Book.objects.filter(id=orderBook.book.id)
    for book in books:
      book.countInLibrary += 1
      book.save()
    return Response('Book Returned Successfully')
  else:
    return Response({'detail': 'Book is not Borrowed out for return'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateBorrowBook(request, pk):
  order = Order.objects.get(id=pk)
  if order.orderState == "Pending":
    order.orderState = "Approved"
    order.accpetedAt = datetime.now()
    order.status = "Borrowed"
    order.save()
    orderBooks = OrderBook.objects.filter(order=order.id)
    for orderBook in orderBooks:
      books = Book.objects.filter(id=orderBook.book.id)
    for book in books:
      book.countInLibrary -= 1
      book.save()
    return Response('Book borrwowed out successfully')
  else:
    return Response({'detail': 'Book Borrowed out already for this order'}, status=status.HTTP_400_BAD_REQUEST)