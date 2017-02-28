from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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

api_key = 'f1927cdc-37b5-4e21-a14e-eb23cd93157c'
url = 'https://api-snacks.nerderylabs.com/v1/snacks?ApiKey=' + api_key

def load_json():
    """Retrieve snack item data from the Web service"""
    # Get json data from Web API, convert data to Python dictionary if valid
    try:
        json_obj = urllib2.urlopen(url)
        return json.loads(json_obj.read())
    except urllib2.HTTPError:
        return None


def handle_error():
    """Error handling for server maintenance"""
    return HttpResponse(
        '<p>The server in undergoing maintenance. Please check back later</p>'
    )


def index(request):
    # Retrieve snack item data
    data = load_json()
    if data:
        # Iterate through snack data, retrieving always purchased snacks
        alwaysPurchasedSnacks = []

        for item in data:

            if not item['optional']:
                alwaysPurchasedSnacks.append(item)

        # Initalize vote count, retrieve cookie data, create session variables
        votesRemaining = 3

        if 'votesRemainingCookie' in request.COOKIES:
            votesRemaining = request.COOKIES['votesRemainingCookie']

        request.session['votesRemainingSession'] = votesRemaining

        suggestedSnacks = snack.objects.filter(optional=True)

        # Render index view, pass voting and snack data to populate tables
        return render(request, 'inventory/index.html', {
            'alwaysPurchasedSnacks': alwaysPurchasedSnacks,
            'suggestedSnacks': suggestedSnacks,
            'votesRemaining': votesRemaining
        })

    else:
        # if valid JSON data wasn't received, handle error
        handle_error()


def suggestions(request):
    # Retrieve snack item data
    data = load_json()
    if data:
        # Retrieve forms
        dropdownSelectionForm = forms.DropdownSelectionForm()
        form = forms.SuggestionForm()

        # Initalize suggestions remaining count, retrieve cookie data
        suggestionsRemaining = 1

        if 'suggestionsRemainingCookie' in request.COOKIES:
            suggestionsRemaining = int(
                request.COOKIES['suggestionsRemainingCookie']
            )

        if suggestionsRemaining < 0:
            suggestionsRemaining = 0

        if request.method == 'POST':  # If user clicks the suggestion button
            dropdownSelectionForm = forms.DropdownSelectionForm(request.POST)
            form = forms.SuggestionForm(request.POST)

            # When user selects dropdown item, check votes remaining
            if (
                request.POST.get('dropDownSuggestion') and
                dropdownSelectionForm.is_valid()
            ):

                if suggestionsRemaining > 0:
                    # Add selection to db
                    for item in data:
                        ddIem = dropdownSelectionForm.cleaned_data['selection']

                        if (
                            int(item['id']) == (
                                int(ddIem)
                            )
                        ):
                            s = snack(
                                id=item['id'], name=item['name'],
                                optional=item['optional'],
                                purchaseLocations=item['purchaseLocations'],
                                purchaseCount=item['purchaseCount'],
                                lastPurchaseDate=item['lastPurchaseDate'],
                            )
                            if item['lastPurchaseDate'] is None:
                                s.lastPurchaseDate = 'Never Purchased'

                            s.save()

                            # decrement suggestions remaining, update cookie
                            suggestionsRemaining -= 1
                            msg = 'Your suggestion \'{0}\' ' \
                                'has been added!'.format(item['name'])
                            messages.success(request, msg)
                            response = HttpResponseRedirect(reverse('index'))
                            response.set_cookie(
                                'suggestionsRemainingCookie',
                                suggestionsRemaining,
                            )
                            return response
                else:
                    # Handles case where user has no suggestions remaining
                    response = HttpResponseRedirect(reverse('index'))
                    messages.error(
                        request, 'You have no more suggestions this month',
                    )
                    return response

            # Handle 'suggest a new snack' form
            elif request.POST.get('formSuggestion'):

                if form.is_valid():
                    if suggestionsRemaining > 0:

                        # Add suggested snack to Web service
                        result = {
                            "name": form.cleaned_data['snack_name'],
                            "location": form.cleaned_data['purchase_locations'],
                            "lattitude": 43.2,
                            "longitude": -89.5677
                        }

                        data = json.dumps(result).encode('utf8')
                        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
                        response = urllib2.urlopen(req)

                        # Add suggested snack to db if it doesn't exist
                        if not snack.objects.filter(
                            name=form.cleaned_data['snack_name'],
                        ).exists():
                            s = snack(
                                name=form.cleaned_data['snack_name'],
                                optional=True,
                                purchaseLocations=(
                                    form.cleaned_data['purchase_locations'],
                                ),
                                purchaseCount=0,
                                lastPurchaseDate='Never Purchased',
                            )
                            s.save()
                            msg = 'Your suggestion \'{0}\' has beeen added!'\
                                .format(form.cleaned_data['snack_name'])

                            messages.success(request, msg)

                            # Decrement suggestions remaining, update cookie
                            suggestionsRemaining -= 1
                            response = HttpResponseRedirect(reverse('index'))
                            response.set_cookie(
                                'suggestionsRemainingCookie',
                                suggestionsRemaining,
                            )
                            return response

                        else:
                            # Handle case where snack is already suggested
                            msg = '\'{0}\' has already been suggested '\
                                'for this month.\n'\
                                'Please suggest a new snack!'\
                                .format(form.cleaned_data['snack_name'])

                            messages.error(request, msg)
                            return HttpResponseRedirect(reverse('suggestions'))

                    else:
                        # Handle case of no suggestion remaining
                        messages.error(
                            request, 'You have no more suggestions this month',
                        )
                        return HttpResponseRedirect(reverse('index'))

        # Retrieve number of optional snacks
        from inventory.forms import get_optional_snacks
        choiceCount = len(get_optional_snacks())

        # Render index view, pass voting and snack data to populate tables
        return render(request, 'inventory/suggestions.html', {
            'form': form,
            'suggestionsRemaining': suggestionsRemaining,
            'dropdownSelectionForm': dropdownSelectionForm,
            'choiceCount': choiceCount,
            })

    else:
        # If valid JSON data wasn't received, handle error
        handle_error()


def vote(request):
    # Retrieve votes remaining session variable
    votesRemaining = int(request.session.get('votesRemainingSession'))

    # Increment vote count for selected item if votes remain, update cookie
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
    response.set_cookie('votesRemainingCookie', votesRemaining)
    return response
