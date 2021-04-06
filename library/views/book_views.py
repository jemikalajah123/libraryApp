from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from library.models import Book,Order,OrderBook
from library.serializers import BookSerializer
from rest_framework import status

contents_per_page = 10

@api_view(['GET'])
def getBooks(request):
  query = request.query_params.get('keyword')
  if query == None:
    query = ''
  Books = Book.objects.filter(
    title__icontains=query).order_by('-createdAt')
  page = request.query_params.get('page')
  paginator = Paginator(Books, contents_per_page)

  try:
    Books = paginator.page(page)
  except PageNotAnInteger:
    Books = paginator.page(1)
  except EmptyPage:
    Books = paginator.page(paginator.num_pages)

  if page == None:
    page = 1

  page = int(page)
  print('Page:', page)
  serializer = BookSerializer(Books, many=True)
  return Response({'Books': serializer.data, 'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBorrowedBooks(request):
  user = request.user
  orders = Order.objects.filter(user=user)
  for order in orders:
    if order.status == "Returned":
      orderBooks = OrderBook.objects.filter(order=order.id)
  for orderBook in orderBooks:
    book = Book.objects.filter(id=orderBook.book.id)
  serializer = BookSerializer(book, many=True)
  return Response(serializer.data)


@api_view(['GET'])
def getBook(request, pk):
  book = Book.objects.get(id=pk)
  serializer = BookSerializer(book, many=False)
  return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createBook(request):
  user = request.user
  data = request.data
  book = Book.objects.create(
    user=user,
    title=data['title'],
    quantity=data['quantity'],
    countInLibrary=data['quantity'],
    isAvailable=True,
    description=data['description']
  )
  serializer = BookSerializer(book, many=False)
  return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    data = request.data
    book.title=data['title']
    book.quantity=data['quantity']
    book.isAvailable=data['isAvailable']
    book.description=data['description']
    book.status = data['status']
    book.save()
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteBook(request, pk):
  book = Book.objects.get(id=pk)
  book.delete()
  return Response('Booked Deleted')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadImage(request):
  data = request.data
  book_id = data['book_id']
  book = Book.objects.get(id=book_id)
  book.image = request.FILES.get('image')
  book.save()
  return Response('Image was uploaded')

