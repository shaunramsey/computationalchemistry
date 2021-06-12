# created by Shaun D Ramsey - 2021 
# version 06.11.21 the output filename can be tied to the input file name, imported logger unifying with frequency.py
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
from logger import log, log_close, log_setup, LogSingleton


program_name = "Geometry Output"
DEFAULT_FILENAME_EXTENSION = ".txt"

log_setup("geometryinput")
    
   

log(' **************************************** ', 1)
log(f" Welcome to {program_name}", 1)
log('   Input is expected to be an opt file, extension .log', 1)
log("   Output is expected to be a generic txt file intended to go in a .com", 1)
log('   You may use any extensions for these files in your execution.', 1)
log(' To run this command use: ', 1)
log(' **** python3 geometryinput.py [optfile.log] -o <outputfile.txt>', 1)
log('   [] is required <> is optional ', 1)
log(' Current DEBUG/VERBOSITY LEVEL: ' + str(LogSingleton().VERBOSITY), 2)
if len(sys.argv) < 2:
    log("    [*] Error, expected at least two arguments", 0)
    sys.exit(1)
log(' **************************************** ', 1)

outputfilename = sys.argv[1]
x = outputfilename.rfind(".")
outputfilename = outputfilename[:x] + DEFAULT_FILENAME_EXTENSION
if outputfilename == sys.argv[1]: #a little sanity check
    outputfilename = "(output)" + outputfilename
    
if len(sys.argv) == 4:
    outputfilename = sys.argv[3]

log( f" [BGN] OUTPUT TO \"{outputfilename}\" BEGINS ", 1)
# go ahead read in the file
with open(sys.argv[1], 'r') as readfile:
    read_data = readfile.read()

output_file = open(outputfilename, 'w')

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
log( f" [END] OUTPUT TO \"{outputfilename}\" COMPLETE ", 1)
log( f" [END] Closing \"{program_name}\".", 1)
log(' **************************************** ', 1)

log_close()
