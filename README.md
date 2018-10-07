# tbcreator
Python3 script to create SystemVerilog testbenche skeletons. Again, it uses version 3 of Python

tbcreatorExample.py contains all the instructions to use the project.
It is suggested to make a copy of it and start by editing it.

To date, tbcreator creates the skeleton of the classes (drivers, monitors, scoreboard,...) needed for a basic yet well-structured testbench and connects it to a DUT. In a very ideal scenario, the user has only to add the behaviour of the components.
The DUT is supposed to be in SystemVerilog and to use interfaces, so manual adjustments may be needed.


The project is HIGHLY experimental and does not exploit all the potentiality of SystemVerilog.
Any suggestion is appreciated.
