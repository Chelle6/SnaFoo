# SnaFoo Snack Suggestion and Voting Applicaiton

A web application built in Python using the Django framework that allows employees at a company to suggest snacks that the Food Services department can purchase that month.  Employees can choose from a list of optional snacks or suggest their own and provide information about where to purchase those snacks.  Employees are limited to 1 snack per month.  Employees also use the SnaFoo system to vote on snacks that have already been suggested for the month.  Employees are allowed 3 votes per month.  Employees can also see a list of snacks that are always purchased by the Food Services department as well.  

## Screen Shots

![votepage_vote_added](https://cloud.githubusercontent.com/assets/12975254/23692389/ceb02072-0393-11e7-9c52-6048bd2b1551.png)
<p align="center">Employee has voted on a snack</p><br />


![votepage_sugestion_added](https://cloud.githubusercontent.com/assets/12975254/23692478/96755712-0394-11e7-8f8c-3a9dc375df6d.png)
<p align="center">Employee has suggested a snack</p><br />


![suggestionspage_dropdown](https://cloud.githubusercontent.com/assets/12975254/23692584/3d80d108-0395-11e7-99fc-90c11d0492fd.png)
<p align="center">Employee selects a snack from dropdown</p><br />


### Technical Specifications

SnaFoo was built using the Django framework 1.10.4 running Python 2.7.10.  

#### Voting

The Voting page shows the snacks currently being purchased or suggested for purchase for the coming month. This consist of two separate lists: those that are always purchased and those that have been suggested so far this month by employees. Each of the suggestions display the current number of votes for that snack this month and the last time the snack was purchased.

Each suggestion has a vote button that allows an employee to vote for a snack. Once an employee's vote has been entered, the employee cannot change their vote.  Employees vote for up to 3 snacks per month. The number of votes remaining for the employee is displayed on the page. If an employee attempts to vote more than 3 times, an error message is displayed indicating that they may not vote until the next month.

Django cookies are used to track whether an employee has used their maximum number of votes.

#### Suggestions

The Suggestions page displays a dropdown from which an employee may select a snack to add to the list of suggested snacks for the month. The source for the items in this menu is set of optional snacks returned by a web service.  This dropdown does not include snacks which are always purchased or snacks which have already been suggested for the month.
There is a Django form that allows an employee to suggest a snack and where it can be purchased if their preferred snack is not listed in the dropdown.  Employee suggestions can be added via a web service as optional snacks for future consideration.

An employee can choose one snack from the list or enter a new snack, not both, per month. 

Once the employee chooses or enters their suggestion, they click the Suggest button to record their suggestion. The application does not allow duplicate suggestions, and form validation ensures that the user has entered all required data when making their suggestion. Error messages are also displayed if an employee attempts to make more than 3 suggestions per month.

#### Web Service

A web service API is used to retrieve the current list of snack foods, some of which are always purchased and some of which are optional.  The API stores this data in JSON format along with additional parameters including how many times that snack has been purchased in the past, where the snack can be purchased, and the last date that the snack was purchased.

The web service also offers the ability to create a new snack entry.

The application validates data retrieved from the service and handles server errors appropriately.

#### Coding Style

The application follows PEP8 code style; HTML 5 was used with the site design.

## Built With

* [Django](http://www.djangoproject.com/) - The web framework used
* [Python](https://python.org/) - The development language used
* [Sublime Text](https://sublimetext.api/) - The code editor used


## Authors

* **Michelle Blanchard** - *Public code repos* - [Chelle6](https://github.com/Chelle6)
