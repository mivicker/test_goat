from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item, List

def home_page(request):
	return render(request, 'home.html')

def view_list(request, list_id):
	list_ = get_object_or_404(List, id=list_id)
	return render(request, 'list.html', {'list': list_})

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST["item_text"], list=list_)
	return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
	list_ = get_object_or_404(List, id=list_id)
	Item.objects.create(text = request.POST["item_text"], list=list_)
	return redirect(f'/lists/{list_.id}/')