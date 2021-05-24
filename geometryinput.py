# created by Shaun D Ramsey - 2021 
# TODO 05.24.21 - include logger.py support for better logging.
# version 05.13.21 includes parsing of geom data and output to file
# licensed under the MIT license - an example of which is: https://opensource.org/licenses/MIT

# Copyright 2021 Shaun D Ramsey
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the "Software"), to deal in the Software without 
# restriction, including without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or 
# substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.

import sys #needed for argv
from datetime import date

#sets the verbosity level for the program, 0 is OFF, 9 is fully verbose/debug
# 0 only errors print generally
# 1 normal verbosity
# 2 lowest level of debug - debug items generally print once
# 5 middle level - status updates in loops and the like
# 9 SHOW ME EVERY DEBUG EVER!
# if you want logs to go to a file, change LOGFILE to True
LOGFILE = True
VERBOSITY = 1
program_name = "Geometry Output"

today = date.today()
LOGFILENAME = "geometryinput"
LOGFILE_OBJ = None
d1 = today.strftime("%d%m%Y")
FULL_LOGFILENAME = LOGFILENAME + d1 + ".log"



def log(msg, level):  
    if VERBOSITY >= level:
        if level > 1:
            msg = f' [{level}]: {msg}'
        elif level == 0:
            msg = f" [ERROR]: {msg}"

    if VERBOSITY >= level:
        print(msg)
    if LOGFILE:
        if LOGFILE_OBJ:
            LOGFILE_OBJ.write(f"[{level}]: {msg}\n")
        else:
            log(" Something went wrong with the log file", 0)

if LOGFILE: #open file for logging
    LOGFILE_OBJ = open(FULL_LOGFILENAME,"a")
    log(f' ** RUN BEGINS **', 999)
    log(f' OPENING LOGFILE "{FULL_LOGFILENAME}"', 2)
    
   

log(' **************************************** ', 1)
log(f" Welcome to {program_name}", 1)
log(' Input is expected to be an opt file, extension .log', 1)
log(" Output is expected to be a generic txt file intended to go in a .com", 1)
log(' You may use any extensions for these files in your execution.', 1)
log(' To run this command use: ', 1)
log(' geometryinput [optfile.log] [outputfile.txt]', 1)
log(' Both inputs are required ', 1)
log(' Current DEBUG/VERBOSITY LEVEL: ' + str(VERBOSITY), 2)
if len(sys.argv) < 3:
    log(" [*] Error, expected three arguments", 0)
    sys.exit(1)
log(' **************************************** ', 1)
log( f" [BGN] OUTPUT TO \"{sys.argv[2]}\" BEGINS ", 1)
# go ahead read in the file
with open(sys.argv[1], 'r') as readfile:
    read_data = readfile.read()

output_file = open(sys.argv[2], 'w')

#\\ is actually an escape code for backslash..tricky
#find the \\Version bits
version_index = read_data.find("\\\\Version")
version_index = version_index - 1
log(F"found \\Version at {version_index} last character: {read_data[version_index]}", 3)

#find the previous \\ bits so we know where the good stuff exists
previous_slashes = read_data.rfind("\\\\", 0, version_index)
previous_slashes = previous_slashes + 2
log(f"Found start at {previous_slashes} First character: {read_data[previous_slashes]}", 3)


# we sub'd this one before and now it may 
# seems strange to have to add the +1 back here, but 0 based indexing and the way splits work
log(f"full data: {read_data[previous_slashes:version_index + 1]}", 9)
data = read_data[previous_slashes:version_index + 1]

#let's remove all newlines and feeds from the data
data = data.replace("\r", "")
data = data.replace("\n", "")
data = data.replace(" ", "")
# file format #,#
# \TYPE, coord, coord, coord  -- repeated until end

#first the non loopy part
prev = 0
idx = data.find(",")
charge1 = data[prev:idx]

# previous idx is idx +1 (skip over the , or slash)
# and next idx will be whatever we're looking for next
prev, idx = idx + 1, data.find("\\", idx + 1)
charge2 = data[prev:idx]

log(f"charges are {charge1}, {charge2}", 2)
output_file.write(f"{charge1} {charge2}\n")

count = 0
log(f"Length of data={len(data)}", 7)
log(f"Lines guesses = {len(data)/40}", 7)

while idx != -1 and idx < len(data):
    log( f" (*) Current count loop is {count}", 3)
    prev, idx = idx + 1, data.find("\\", idx + 1)
    if idx == -1: 
        idx = len(data)
    log( f"indices found are: {prev}:{idx}", 8)
    log( f"the data found is: {data[prev:idx]}", 7)

    dica = data[prev:idx]
    dica = dica.split(",")
    log( f"array is {dica[0]} {dica[1]} {dica[2]} {dica[2]} ", 7)

    output_file.write(f"{dica[0]:<4} {dica[1]:>15} {dica[2]:>15} {dica[3]:>15}\n")


    count = count + 1



output_file.close()
log( f" [END] OUTPUT TO \"{sys.argv[2]}\" COMPLETE ", 1)
log( f" [END] Closing \"{program_name}\".", 1)
log(' **************************************** ', 1)


if LOGFILE:
    log(' CLOSING LOGFILE ', 2)
    log(' RUN ENDS \n', 999)
    LOGFILE_OBJ.close()
