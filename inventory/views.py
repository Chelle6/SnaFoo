from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse
import json
from inventory.models import snack
from django.contrib import messages
import urllib
from . import forms
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2

# import urllib
# # import urllib2
# import json
# import requests
# from django.http import JsonResponse

api_key = 'f1927cdc-37b5-4e21-a14e-eb23cd93157c'
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

	
	alwaysPurchasedSnacks = []


	for item in data:


		if item['optional'] == False:
			alwaysPurchasedSnacks.append(item)
			

		# if not snack.objects.filter(name=item['name']).exists(): # if the object doesn't exist
		# 	s = snack(name=item['name'], optional=item['optional'], purchaseLocations=item['purchaseLocations'], purchaseCount=item['purchaseCount'], lastPurchaseDate=item['lastPurchaseDate'], id=item['id'])
		# 	s.save()

	votesRemaining = 3

	if 'votesRemainingCookie' in request.COOKIES:  # if votesRemainingCookie exists
		votesRemaining = request.COOKIES['votesRemainingCookie']  # update votesRemaining to cookie value

	request.session['votesRemainingSession'] = votesRemaining

	#alwaysPurchasedSnacks = snack.objects.filter(optional=False)
	suggestedSnacks = snack.objects.filter(optional=True)

	return render(request, 'inventory/index.html', {
		#'items': items,
		'alwaysPurchasedSnacks': alwaysPurchasedSnacks,
		'suggestedSnacks': suggestedSnacks,
		'votesRemaining': votesRemaining
	})

def suggestions(request):
	form = forms.SuggestionForm()
	if request.method =='POST':  # if you click the suggestion button
		form = forms.SuggestionForm(request.POST)  # pass data to form model
		if form.is_valid():
			# result = {
			#     "name": form.cleaned_data['snack_name'],
			#     "location": form.cleaned_data['purchase_locations'],
			#     "lattitude": 43.2,
			#     "longitude": -89.5677
			# }

			# data = json.dumps(result).encode('utf8')  # convert dictionary to json
			# req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
			# response = urllib2.urlopen(req)
			

			if not snack.objects.filter(name=form.cleaned_data['snack_name']).exists(): # if the object doesn't exist
				s = snack(name=form.cleaned_data['snack_name'], optional=True, purchaseLocations=form.cleaned_data['purchase_locations'],
					purchaseCount=0, lastPurchaseDate='Never Purchased')
				s.save()

				messages.success(request, 'Your suggestion \'{0}\' has beeen added!'.format(form.cleaned_data['snack_name']))
				return HttpResponseRedirect(reverse('index'))
			else:
				messages.error(request, '\'{0}\' has already been suggested for this month! <br>Please suggest A new snack'.format(form.cleaned_data['snack_name']))
				return HttpResponseRedirect(reverse('suggestions'))


	return render(request, 'inventory/suggestions.html', {	'form' : form,
	})


def vote(request):
	votesRemaining = int(request.session.get('votesRemainingSession'))
	if votesRemaining > 0:
		votesRemaining -= 1

		selected_choice = snack.objects.get(id=request.POST['snack'])
		selected_choice.votes += 1
		selected_choice.save()

		messages.success(request, 'Your vote has beeen added!')
	else:
		votesRemaining = 0
		messages.error(request, 'You have used all of your votes this month')
		

	response = HttpResponseRedirect(reverse('index'))
	response.set_cookie('votesRemainingCookie', 3)
	return response