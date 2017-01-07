from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse



def index(request):
	items = Item.objects.exclude(amount=0)
	return render(request, 'inventory/index.html', {
		'items': items,
	})


	return HttpResponse('<p>In index view</p>')
