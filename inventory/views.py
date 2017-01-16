from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from inventory.models import snack
from django.core.urlresolvers import reverse

def index(request):
	#items = snack.objects.all()
	
	alwaysPurchasedSnacks = snack.objects.filter(optional=False)
	suggestedSnacks = snack.objects.filter(optional=True)


	return render(request, 'inventory/index.html', {
		#'items': items,
		'alwaysPurchasedSnacks': alwaysPurchasedSnacks,
		'suggestedSnacks': suggestedSnacks,
	})

def results(request):
	suggestedSnacks = snack.objects.filter(optional=True)

	return render(request, 'inventory/results.html', {
		'suggestedSnacks': suggestedSnacks,
	})


def vote(request):
	selected_choice = snack.objects.get(id=request.POST['snack'])
	selected_choice.votes += 1
	selected_choice.save()

	return HttpResponseRedirect(reverse('results'))