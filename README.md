# computationalchemistry
scripts for computational chemistry

Grab the latest python3 version from: https://www.python.org/downloads/

Then, from this repository, grab the three py files. frequency.py and geometryinput.py rely on logger.py for logging capabilities.
Stick them in a directory that you'd like to run the programs from. Output will likely be in the current working directory, so you may want to stick them in your path/bin.

Open your terminal and get started!

Example executions:

python3 frequency.py Freq_ex1.log

and

python3 geometryinput.py Opt_ex1.log


By default, frequency.py will output to a .txt, but you may add -o filename to pick a specific filename that you enjoy.
By default, geometryinput.py will output to a .csv file, but you can use -o filename to pick a specific filename that you enjoy.
