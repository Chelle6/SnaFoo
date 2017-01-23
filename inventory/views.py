from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse
import json
from inventory.models import snack
#import urllib
# from . import forms
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2

# import urllib
# # import urllib2
# import json
# import requests
# from django.http import JsonResponse

api_key = '24f93691-f294-4165-b731-660c160b1919'
url = 'https://api-snacks.nerderylabs.com/v1/snacks?ApiKey=' + api_key
# json_obj = urllib2.urlopen(url)
# data = json.loads(json_obj.read())

# alwaysPurchasedSnacks = []
# suggestedSnacks = []

# for item in data:
# 	if item['optional'] == False:
# 		suggestedSnacks.append(item)
# 	else:
# 		alwaysPurchasedSnacks.append(item)

def index(request):
	json_obj = urllib2.urlopen(url) # get json data from Web API
	data = json.loads(json_obj.read().decode('utf8'))  # convert json data to Python dictionary

	for item in data:
		if not snack.objects.filter(name=item['name']).exists(): # if the object doesn't exist
			s = snack(name=item['name'], optional=item['optional'], purchaseLocations=item['purchaseLocations'], purchaseCount=item['purchaseCount'], lastPurchaseDate=item['lastPurchaseDate'], id=item['id'])
			s.save()
	# votesRemaining = 3

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