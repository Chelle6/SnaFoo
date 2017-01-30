from django import forms

class SuggestionForm(forms.Form):
    name = forms.CharField(max_length=200)
    purchase_locations = forms.CharField(widget=forms.Textarea, max_length=50)