from django import forms
import json
import urllib
#from . import forms
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2


def get_my_choices():
	my_choices = []
	api_key = 'f1927cdc-37b5-4e21-a14e-eb23cd93157c'
	url = 'https://api-snacks.nerderylabs.com/v1/snacks?ApiKey=' + api_key
	json_obj = urllib2.urlopen(url) # get json data from Web API
	data = json.loads(json_obj.read().decode('utf8'))  # convert json data to Python dictionary
	for item in data:
		if item['optional'] == True:


			optionalSnack = (item['id'], item['name']) # tuple
			my_choices.append(optionalSnack)

	return my_choices


class SuggestionForm(forms.Form):
    snack_name = forms.CharField(max_length=200, required=False)
    purchase_locations = forms.CharField(widget=forms.Textarea, max_length=50, required=False)


class DropdownSelectionForm(forms.Form):
	selection = forms.ChoiceField(choices=get_my_choices, widget=forms.Select, required=False)