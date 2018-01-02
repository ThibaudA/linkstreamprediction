# Link Stream Prediction  

Activity prediction in link streams algorithm

## Getting Started

### Prerequisites

```
Python3
Numpy
Scipy
Matplotlib
```

##Data structure

Undirected link stream

Format:

```
t u v
...
```

(float) t : time of the link
(int,int) u v : pair of nodes

## Running the prediction.

```
cat dataset | python main.py configfile
```


Configuration file structure:
```
(float) #start time of observation training period
(float) #end time of observation training period
(float) #start time of prediction training period
(float) #end time of prediction training period
(float) #start time of observation
(float) #end time of observation
(float) #start time of pred
(float) #end time of pred
Metrics #Metrics used:
Metric1 [parameters]
Metric2 [parameters]
Metric3 [parameters]
EndMetrics
Commentaries:
Bla bla
```

Metrics available:

```
benchMark
commonNeighbors
weightedCommonNeighbors
resourceAlloc
weightedResourceAlloc
adamicAdar
weightedAdamicAdar
sorensenIndex
weightedSorensenIndex
benchMarkReduxNbLinksk
benchMarkReduxTimeInterk"
```
[parameters]: (int,in) 
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
