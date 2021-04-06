# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class UserType(models.Model):
  name = models.CharField(max_length=200, unique=True)
  isActive = models.BooleanField(default=True)
  updatedAt = models.DateTimeField(auto_now=True)
  createdAt = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


class Book(models.Model):
  good = "Good"
  faulty = "Faulty"

  STATUS = (
    (good, faulty),
    (faulty, faulty),
  )

  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  image = models.ImageField(null=True, blank=True)
  title = models.CharField(max_length=200, null=True, blank=True)
  quantity = models.IntegerField(null=True, blank=True, default=0)
  isAvailable = models.BooleanField(default=False)
  description = models.TextField(null=True, blank=True)
  status = models.CharField(max_length=100, choices=STATUS, default=good)
  countInLibrary = models.IntegerField(null=True, blank=True, default=0)
  updatedAt = models.DateTimeField(auto_now=True)
  createdAt = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title


class Order(models.Model):
  pending = 'Pending'
  approved = 'Approved'
  rejected = 'Rejected'

  STATE = (
    (pending, pending),
    (approved, approved),
    (rejected, rejected)
  )

  borrowed = 'Borrowed'
  returned = 'Returned'

  STATUS= (
    (borrowed, borrowed),
    (returned, returned),
  )
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  orderState = models.CharField(max_length=10, choices=STATE, default=pending)
  returnDate = models.DateTimeField(auto_now_add=False)
  accpetedAt = models.DateTimeField(auto_now_add=False, null=True)
  status = models.CharField(max_length=100, choices=STATUS, null=True)
  updatedAt = models.DateTimeField(auto_now=True)
  createdAt = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.createdAt)

class OrderBook(models.Model):
  book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  updatedAt = models.DateTimeField(auto_now=True)
  createdAt = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.createdAt)
