from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

from Base.forms import RoomForm, CreateUserForm, UserForm
from Base.models import User, Room, Topic, Message


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topic = Topic.objects.all()[:4]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[:3]

    context = {'rooms': rooms, 'topics': topic, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'Base/home.html', context)


def profile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topic = Topic.objects.all()[:4]

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topic}

    return render(request, 'Base/profile.html', context)


@login_required(login_url='Login')
def createRoom(request):
    form = RoomForm()
    topic = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        messages.success(request, f"Room Created with the name: {request.POST.get('name')}")
        return redirect('Home')

    context = {'form': form, 'topics': topic}
    return render(request, 'Base/room_form.html', context)


@login_required(login_url='Login')
def updateRoom(request, id):
    edit = True
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return redirect('Home')

    form = RoomForm(instance=room)
    topic = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        messages.success(request, f"Room updated with the name: {request.POST.get('name')}")
        return redirect('Home')

    context = {'form': form, 'topics': topic, 'room': room, 'edit': edit}
    return render(request, 'Base/room_form.html', context)


@login_required(login_url='Login')
def deleteRoom(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        messages.warning(request, "Unauthorized accessed")
        return redirect('Home')

    if request.method == 'POST':
        room.delete()
        messages.success(request, f"'{Room}' deleted successfully")
        return redirect('Home')

    return render(request, 'Base/delete.html', {'obj': room})


def room(request, id):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        messages.success(request, "Message published")
        return redirect('Room', id=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}

    return render(request, 'Base/room.html', context)


@login_required(login_url='Login')
def deleteMessage(request, id):
    message = Message.objects.get(id=id)

    if request.user != message.user:
        messages.warning(request, "Unauthorized accessed")
        return redirect('Home')

    if request.method == 'POST':
        message.delete()
        messages.success(request, f"{message} deleted successfully")
        return redirect('Home')

    return render(request, 'Base/delete.html', {'obj': message})


def registerUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "Registered Successfully")
            return redirect('Home')
        else:
            messages.error(request, 'An error occurred during registration (Try Again) ')

    return render(request, 'Base/login_register.html', {'form': form})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('Profile', id=user.id)

    return render(request, 'Base/update_user.html', {'form': form})


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Invalid Credential")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect('Home')
        else:
            messages.error(request, "Invalid Credential")

    return render(request, 'Base/login_register.html', {'page': page})


@login_required(login_url='Login')
def logoutUser(request):
    logout(request)
    return redirect('Home')


def topics(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    topic = Topic.objects.filter(Q(name__icontains=q))
    return render(request, 'Base/topics.html', {'topics': topic})


def activity(request):
    room_messages = Message.objects.all()[:3]
    return render(request, 'Base/activity.html', {'room_messages': room_messages})
