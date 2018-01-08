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

### Default settings

Prediction with and without classes

3 classes by pair activity:
```
  C0: without classes
  C1: pair without interaction during observation
  C2: less than classthreshold=5 links during observation
  C3: more than classthreshold=5 links during observation
  AllClasses: Union of C1, C2 and C3
```

* Activity extrapolation during training: Activity during training prediction period
* Activity extrapolation during real prediction: Extrapolation of observation period activity
* Gradient descent initiation: Random exploration of the parameters space between the parameters indicated in the configuration file for each metric


### Data structure

Undirected link stream

Format:

```
t u v
...
```

\<float:t\> : time of the link

\<int:u\>,\<int:v\> : pair of nodes

## Running the prediction

```
cat <data_file>  | python main.py <config_file>
```

Configuration file structure:
```
<float:tstartobsT> #start time of observation training period
<float:tendobsT> #end time of observation training period
<float:tstartpredT> #start time of prediction training period
<float:tendpredT> #end time of prediction training period
<float:tstartobs> #start time of observation
<float:tendobs> #end time of observation
<float:tendpred> #end time of pred
Metrics #Metrics used:
Metric1 [parameters]
Metric2 [parameters]
Metric3 [parameters]
EndMetrics
[Options]
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
benchMarkReduxNbLinks<int:k>
benchMarkReduxTimeInter<int:k>"
```

parameters: (int),(int)

## Output:

By default the algorithm output the prediction quality and the metric combination used by during the prediction by classes.
The list of predicted links can be extracted via the "Extract" option (see below)

## Other settings:

* Prediction extraction (In configuration file : [Option] = Extract \<directory\>)
* Number of step during random exploration (Variables: RENbstep and REPNbstep)
* Max number of step during gradient descent (Variables: GDMaxstep and GDPMaxstep)
* Fine tuning of gradient descent (derstep, sizelinexptep and numlinexptep )
* One step prediction using the the parameters indicated in the configuration file for each metric (In config file : [Option] = Onepred)



<!-- ### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```



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
-->
