from tokenize import group
from unicodedata import name
from django.shortcuts import render
from .models import Group , Chat
# Create your views here.
def home(request):
    return render(request,'app/index.html')


def channels(request , group_name):
    group_present = Group.objects.filter(name=group_name).first()
    chat_msgs = []
    if group_present:
        chat_msgs = Chat.objects.filter(group = group_present)
    else:
        create_group = Group(name=group_name)
        create_group.save()
    context = {"gropuname":group_name,"chat_msgs":chat_msgs}
    return render(request,'app/channels.html',context)