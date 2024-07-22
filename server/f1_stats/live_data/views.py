from django.shortcuts import render

def index(request):
    return render(request, "live_data/index.html")

def room(request, room_name):
    return render(request, "live_data/index.html", {"room_name": room_name})
