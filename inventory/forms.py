from django import forms
from inventory.models import snack
import json
import urllib

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


def get_optional_snacks():
    """Retrieve list of optional snacks to populate the dropdown"""
    optional_snacks = []

    # Retrieve all snacks from Web service
    from inventory.views import get_url
    json_obj = urllib2.urlopen(get_url())
    data = json.loads(json_obj.read())

    # If optional snacks don't exist in db, add snack to dropdown
    for item in data:
        if (
            item['optional'] and
            not snack.objects.filter(id=item['id']).exists()
        ):

            optional_snack = (item['id'], item['name'])
            optional_snacks.append(optional_snack)

    return optional_snacks


class SuggestionForm(forms.Form):
    snack_name = forms.CharField(max_length=200)
    purchase_locations = forms.CharField(widget=forms.Textarea, max_length=50)


class DropdownSelectionForm(forms.Form):
    selection = forms.ChoiceField(
        choices=get_optional_snacks,
        widget=forms.Select,
        required=False,
    )
