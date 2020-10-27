# Version History #

## HEAD ##

* Bumped version number to 0.2.
* Added installation instructions, example usage and improved the python setup script.
* Updated the equation to compute the inferred redshift to a more recent one (Zhang 2018).
* Automatically look up the Milky Way DM contribution for a given event based on the `YMW16` model. The lookup happens fully automatically in the `VOEvent` class.

## 0.1 (2020-03-09) ##

The code was successfully tested in a TUSE to FBFUSE high-level triggering run.

* Use YAML configuration file with default values.
* Convert main part of the code to VOEvent class that has member functions to generate and emit events, among others.
* Added script to emit VOEvents periodically with randomised (but sensible!) parameters. This will be used to test the receiving code.
* Added script to generate VOEvents from the command line.
* Initial docker software configuration, including various VOEvent python tools.
