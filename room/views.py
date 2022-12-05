from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Room, Message


# Create your views here.
@login_required
def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, "room/all.html", {'rooms': rooms})


@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'room/room.html', {'room': room, 'messages': messages})
