from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Room,Topic,Message
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def loginpage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')    
        password = request.POST.get('password')    
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,'Username not available.')
        print(username+password)
        user = authenticate(request,username = username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or password might be wrong ")
    dic = {
        "page":page,
    }
    return render(request,"html/login_register.html",dic)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration.')
    dic={
        "form":form,
    }
    return render(request,'html/login_register.html',dic)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains= q)|
    Q(name__icontains= q) |
    Q(description__icontains= q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains = q))
    dic={
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,    
        'room_messages':room_message
    }
    return render(request,'html/home.html',dic)


def room(request,roomid):
    rooms = Room.objects.get(id = roomid)
    room_messages = rooms.message_set.all().order_by('-created')
    participants = rooms.participants.all()
   
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = rooms,
            body = request.POST.get('body'),
        )
        rooms.participants.add(request.user)
        return redirect('room',roomid=rooms.id)
    dic ={
        'rooms':rooms,
        'room_messages':room_messages,
        'participants':participants,
    }
    return render(request,'html/room.html',dic)


def  userprofile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    dic = {
        "user":user,
        "rooms":rooms,
        "room_messages":room_message,
        "topics":topics,
    }
    return render(request,'html/profile.html',dic)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    dic = {
        "form":form
    }
    return render(request,'html/room_form.html',dic)


@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not allowed here..")
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    dic = {
        "form":form
    }
    return render(request,'html/room_form.html',dic)        


@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here..")
    if request.method =="POST":
        room.delete()
        return redirect('home')
    dic = {
        "obj":room
    }
    return render(request,'html/delete.html',dic)


@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed here..")
    if request.method == "POST":
        message.delete()
        return redirect('home')
    dic = {
        "obj":message,
    }
    return render(request,'html/delete.html',dic)