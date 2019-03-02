Version: Python 2.7
Purpose: Used to send user records and sample records from a client to a server over a given amount of socket connections

Example of command line for HealthServ.py:

    ./HealthServ.py -p 4997 -p 6010 -p 7653 -p 7652

Example of command line for HealthMon.py:

     ./HealthMon.py info.dat 0.0.0.0:4997 0.0.0.0:6010 0.0.0.0:7653 < samples.dat