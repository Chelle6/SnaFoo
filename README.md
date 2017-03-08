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

SnaFoo was built using the Django Framework 1.10.4 running Python 2.7.10.  Optional and always purchased snacks are retrieved from a web service API, packaged as JSON, and parsed by the SnaFoo application.  When a user suggests a snack, either one of their own, or from a Dropdown listing optional snacks returned by the web service, the snack objects are added to a database and initialized to start voting on upon creation.  Django forms are used for suggesting snacks, and the number of snacks an employee can suggest are stored as Python cookie objects.  When a user suggests a snack, the snack item is also added to the web service via and API call formatting the data JSON encoding.  

The voting page retrieves a list of always purchased snacks from the web services and allows employees to vote on snacks which have been suggested for the month.  Logic is implemented to ensure no duplicate snacks have been suggested.  When a user has suggested a snack, the snack's vote count gets updated accordingly along with the number of votes the employee has remaining.

Error handling is also implemented to handle all possible failure occurences, issues such as server maintenance, and instances of when an employee is out of votes remaining or has used their alloted amount of suggestions for the month.




## Built With

* [Django](http://www.djangoproject.com/) - The web framework used
* [Python](https://python.org/) - The development language used
* [Sublime Text](https://sublimetext.api/) - The code editor used


## Authors

* **Michelle Blanchard** - *Public code repos* - [Chelle6](https://github.com/Chelle6)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.
