from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
import json
from inventory.models import snack
from django.contrib import messages
import urllib
from . import forms
from inventory.forms import get_optional_snacks
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

# Error message to de displayed in event data coun't be retrieved
error_msg = '<p>The server in undergoing maintenance. \
Please check back later</p>'


# Return URL of Nerdery webservice
def get_url():
    api_key = 'f1927cdc-37b5-4e21-a14e-eb23cd93157c'
    return 'https://api-snacks.nerderylabs.com/v1/snacks?ApiKey=' + api_key


def index(request):
    # Get json data from Web API, convert data to Python dictionary if valid
    try:
        json_obj = urllib2.urlopen(get_url())
    except urllib2.HTTPError:
        return HttpResponse(error_msg)
    else:
        data = json.loads(json_obj.read())

        # Iterate through snack data, retrieving always purchased snacks
        always_purchased_snacks = []

        for item in data:

            if not item['optional']:
                always_purchased_snacks.append(item)

        # Initalize vote count, retrieve cookie data, create session variables
        votes_remaining = 3

        if 'votes_remaining_cookie' in request.COOKIES:
            votes_remaining = request.COOKIES['votes_remaining_cookie']

        request.session['votes_remaining_session'] = votes_remaining

        suggested_snacks = snack.objects.filter(optional=True)

        # Render index view, pass voting and snack data to populate tables
        return render(request, 'inventory/index.html', {
            'always_purchased_snacks': always_purchased_snacks,
            'suggested_snacks': suggested_snacks,
            'votes_remaining': votes_remaining
        })


def suggestions(request):
    # Retrieve snack item data
    # Get json data from Web API, convert data to Python dictionary if valid
    try:
        json_obj = urllib2.urlopen(get_url())
    except urllib2.HTTPError:
        return HttpResponse(error_msg)
    else:
        data = json.loads(json_obj.read())

        # Retrieve forms
        dropdown_selection_form = forms.DropdownSelectionForm()
        form = forms.SuggestionForm()

        # Initalize suggestions remaining count, retrieve cookie data
        suggestions_remaining = 1

        # if 'suggestions_remaining_cookie' in request.COOKIES:
        #     suggestions_remaining = int(
        #         request.COOKIES['suggestions_remaining_cookie']
        #     )

        if suggestions_remaining < 0:
            suggestions_remaining = 0

        if request.method == 'POST':  # If user clicks the suggestion button
            dropdown_selection_form = forms.DropdownSelectionForm(request.POST)
            form = forms.SuggestionForm(request.POST)

            # When user selects dropdown item, check votes remaining
            if (
                request.POST.get('dropdown_suggestion') and
                dropdown_selection_form.is_valid()
            ):

                if suggestions_remaining > 0:
                    # Add selection to db
                    for item in data:
                        dropdown_item = (
                            dropdown_selection_form.cleaned_data['selection']
                        )

                        if (
                            int(item['id']) == (
                                int(dropdown_item)
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
                            suggestions_remaining -= 1
                            msg = 'Your suggestion \'{0}\' ' \
                                'has been added!'.format(item['name'])
                            messages.success(request, msg)
                            response = HttpResponseRedirect(reverse('index'))
                            response.set_cookie(
                                'suggestions_remaining_cookie',
                                suggestions_remaining,
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
                    if suggestions_remaining > 0:

                        # Add suggested snack to Web service
                        result = {
                            "name":
                                form.cleaned_data['snack_name'],
                            "location":
                                form.cleaned_data['purchase_locations'],
                            "latitude": 43.2,
                            "longitude": -89.5677
                        }

                        data = json.dumps(result).encode('utf8')
                        url = get_url()
                        req = urllib2.Request(
                            url, data, {'Content-Type': 'application/json'}
                        )
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
                            suggestions_remaining -= 1
                            response = HttpResponseRedirect(reverse('index'))
                            response.set_cookie(
                                'suggestions_remaining_cookie',
                                suggestions_remaining,
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
        choiceCount = len(get_optional_snacks())

        # Render index view, pass voting and snack data to populate tables
        return render(request, 'inventory/suggestions.html', {
            'form': form,
            'suggestions_remaining': suggestions_remaining,
            'dropdown_selection_form': dropdown_selection_form,
            'choiceCount': choiceCount,
            })


def vote(request):
    # Retrieve votes remaining session variable
    votes_remaining = int(request.session.get('votes_remaining_session'))

    # Increment vote count for selected item if votes remain, update cookie
    if votes_remaining > 0:
        votes_remaining -= 1

        selected_choice = snack.objects.get(id=request.POST['snack'])
        selected_choice.votes += 1
        selected_choice.save()

        messages.success(request, 'Your vote has beeen added!')

    else:
        votes_remaining = 0
        messages.error(request, 'You have used all of your votes this month')

    response = HttpResponseRedirect(reverse('index'))
    response.set_cookie('votes_remaining_cookie', votes_remaining)
    return response
