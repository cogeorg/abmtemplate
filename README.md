**abm_template** is a template for writing financial agent-based models in python. It uses abstract base classes and is provided with a sample implementation in sample_model.py. The use of abstract based classes, and specifically the abm_template ensures high degree of intercompatibility between agent-based models created based on it. This renders this library particularly useful for institutions or groups of people who create multiple agent-based models, and want to gain extra value from being able to reuse and interchange parts of them in new work easily. The below will explain the structure of the library, the purpose of specific folders and files, as well as the sample implementation. For the documentation of specific functions please see the source code (particularly docstrings and comments).

The main part of the abm_template, as in the template itself, is stored in the **/src/** folder, and contains abstract classes for parts of an abstract agent-based model. These are described below:

- **baseagent.py**:

- **baseconfig.py**:

- **basemarket.py**:

- **basemeasurement.py**:

- **basemodel.py**:

- **baserunner.py**:

- **baseshock.py**:

- **basetransaction.py**:

- **goodness.py**: this one is not a part of the abstract template as such, but is a tool that helps with agent-based models on an abstract level.

The **/configs/** folder has sample config files that are needed by the instances of the abstract classes, these are in particular necessary for BaseConfig, BaseRunner, and goodness. Config files in abm_template are xml files, the structure of these is described within the source code, usually in the docstring of the function reading the config.

The **/samples/** folder consists of sample files necessary for the samples. Currently has mock outputs of an agent-based model, which we use for testing the goodness.py script.

The **/tests/** folder is very important.

In the main folder we have the sample implementation of the abm_template, as described below. We also have the calc_goodness.py file which is a sample implementation of the goodness.py script. Further, the abm_template_tests.py invokes the tests described above.

The sample implementation is very basic and shows to implement the abstract base classes, the implementation is of a simple game with parameter
theta, two agents, two choices of action (1,0) and a payout matrix:

```
  	1				0
1 [	(1-theta,1-theta)		(-theta,0)	]
0 [	(0,-theta)			(0,0)		]
```

There are simple equilibria:
Theta is known to both agents, there is common knowledge about theta.
If theta < 0, both agents find attack the dominant action: unique Nash equilibrium: {1, 1}
If theta > 1, both agents find refrain the dominant action: unique Nash equilibrium: {0, 0}
If theta is between [0, 1] both equilibria can be sustained as pure strategy Nash equilibria.

The main part of the simulation is the sample_model.py which specifies the above, but other classes are also implemented as necessary. The files associated with the sample implementation have names prefixed with sample, thus are easy to find or copy as a lump.

To run the sample implementation use:

```
python sample.py
```

co-pierre.georg@uct.ac.za
pawel.fiedor@uct.ac.za
2016