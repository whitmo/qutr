======
 qutr
======

socketio protocol
=================

Job view
--------
 
lineOut
~~~~~~~
      
raw line of output, display in <li />


dataOut
~~~~~~~

 state
   notifier of a state change for a job
   - queued 
   - starting
   - finished
   - failed

 visualization
   A visualized output
   - load
   - start
   - stop
   - update

 interaction
   An interaction between a job and a user
   - load
   - start
   - response
   - stop


Demo
====

Visualize a deployment
----------------------

using circus, locust, metlog::

 - data source
 - 0-N web apps
 - load testing 
