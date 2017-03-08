# SnaFoo Snack Suggestion and Voting Applicaiton

A web application built in Python using the Django framework that allows employees at a company to suggest snacks that the Food Services department can purchase that month.  Employees can choose from a list of optional snacks or suggest their own and provide information about where to purchase those snacks.  Employees are limited to 1 snack per month.  Employees also use the SnaFoo system to vote on snacks that have already been suggested for the month.  Employees are allowed 3 votes per month.  Employees can also see a list of snacks that are always purchased by the Food Services department as well.  

## Screen Shots

INSERT SCREEN SHOTS

### Technical Specifications

SnaFoo was built using the Django Framework 1.10.4 running Python 2.7.10.  Optional and always purchased snacks are retrieved from a web service API, packaged as JSON, and parsed by the SnaFoo application.  When a user suggests a snack, either one of their own, or from a Dropdown listing optional snacks returned by the web service, the snack objects are added to a database and initialized to start voting on upon creation.  Django forms are used for suggesting snacks, and the number of snacks an employee can suggest are stored as Python cookie objects.  When a user suggests a snack, the snack item is also added to the web service via and API call formatting the data JSON encoding.  

The voting page retrieves a list of always purchased snacks from the web services and allows employees to vote on snacks which have been suggested for the month.  Logic is implemented to ensure no duplicate snacks have been suggested.  When a user has suggested a snack, the snack's vote count gets updated accordingly along with the number of votes the employee has remaining.

Error handling is also implemented to handle all possible failure occurences, issues such as server maintenance, and instances of when an employee is out of votes remaining or has used their alloted amount of suggestions for the month.


```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
