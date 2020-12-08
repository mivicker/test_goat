from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

def home_page(request):
	if request.method == "POST":
		Item.objects.create(text=request.POST["item_text"])
		return redirect('/lists/the-only-list/')

	items = Item.objects.all()
	return render(request, 'home.html', {'items':items})

def view_list(request):
	pass