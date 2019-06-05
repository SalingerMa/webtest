from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from guestapi.serializers import UserSerializer, GroupSerializer
from guestapi.models import Event, Guest
from guestapi.serializers import EventSerializer, GuestSerializer

# Create your views here.

# viewsets 定义视图的展现形式
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer



