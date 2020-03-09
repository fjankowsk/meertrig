# Version History #

## HEAD ##

## 0.1 (2020-03-09) ##

The code was successfully tested in a TUSE to FBFUSE high-level triggering run.

* Use YAML configuration file with default values.
* Convert main part of the code to VOEvent class that has member functions to generate and emit events, among others.
* Added script to emit VOEvents periodically with randomised (but sensible!) parameters. This will be used to test the receiving code.
* Added script to generate VOEvents from the command line.
* Initial docker software configuration, including various VOEvent python tools.
