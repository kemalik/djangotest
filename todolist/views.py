from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Task
from .forms import TaskForm
from django.views.decorators.csrf import csrf_exempt


def index(request):
	tasks = Task.objects.all()
	return render(request, "index.html", {"tasks" : tasks})
		
		
def add(request):
	if request.method == "POST":
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save()
		return HttpResponseRedirect("/")
	else:
		form = TaskForm()
		return render(request, "add.html", {"form" : form})


def edit(request, id):
	task = get_object_or_404(Task, id = id)
	if task.complete == 1:
		return HttpResponseRedirect("/")      
	if request.method == "POST":
		form = TaskForm(request.POST, instance = task)	
		if form.is_valid():
			task = form.save()
			return HttpResponseRedirect("/")
	else:
		form = TaskForm(instance = task)
		return render(request, "edit.html", {"form" : form})


def delete(request, id):
	task = get_object_or_404(Task, id = id)
	task.delete()
	return HttpResponseRedirect("/")


@csrf_exempt
def complete(request):
	if request.method == "POST":
		id = request.POST.get("id")
		task = get_object_or_404(Task, id = id)
		task.complete = True
		task.save()
	return HttpResponseRedirect("/")
	