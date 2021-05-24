# created by Shaun D Ramsey - 2021 
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

import sys
import re
import datetime
from logger import log, log_close, log_setup, LogSingleton
import tkinter as tk
from tkinter import filedialog


GUI = True
program_name = "Frequency/Intensity CSV"

def main_program():

    log_setup("frequency", 1)
   

    log(' **************************************** ')
    log(f" Welcome to {program_name}")
    log(' To use this program use: ')
    log(' frequency [optfile.log] [outputfile.txt]')
    log(' Both inputs are required ')
    log(' Current DEBUG/VERBOSITY LEVEL: ' + str(LogSingleton().VERBOSITY), 2)
    log(' **************************************** ')

    if len(sys.argv) < 3:
        log(" [*] Error, expected three arguments", 0)
        sys.exit(1)

    log( f" [BGN] OUTPUT TO \"{sys.argv[2]}\" BEGINS ", 1)



    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if GUI:
        input_file = inputFilename.get()
        output_file = outputFilename.get()

    f = open(input_file, "r")
    of = open(output_file, "w")

    freq_list = []
    int_list = []

    lines = f.readlines()

    for line in lines:
        if line[0:15] == " Frequencies --":
            number_line = re.sub('\s+', ' ', line[15:])
            number_line = number_line.strip()
            freqs = number_line.split(" ")
            freq_list.extend(freqs)
        if line[0:15] == " IR Inten    --":
            number_line = re.sub('\s+', ' ', line[15:])
            number_line = number_line.strip()
            ints = number_line.split(" ")
            int_list.extend(ints)


    log(f" {freq_list} total length={len(freq_list)} ", 8)
    log(f" {int_list} total length={len(int_list)}", 8)

    log(f"Frequencies    ,   Intensities", 3)
    of.write(f"Frequencies    ,   Intensities\n")
    for i in range(len(freq_list)):
        log(f"{freq_list[i]:<14} ,   {int_list[i]:<14}", 3)
        of.write(f"{freq_list[i]:<14} ,   {int_list[i]:<14}\n")

    of.close()

    log( f" [END] OUTPUT TO \"{sys.argv[2]}\" COMPLETE ", 1)
    log( f" [END] Closing \"{program_name}\".", 1)
    log(' **************************************** ', 1)

    log_close()


if GUI:
    root = tk.Tk()
    root.geometry("400x250")
    root.title("Frequency Correlation")


    inputFilename = tk.StringVar()
    inputFilename.set("Freq_ex1.log")
    if len(sys.argv) > 1:
        inputFilename.set(sys.argv[1])

    outputEntry = tk.Button(textvariable=inputFilename, command=lambda: inputFilename.set(filedialog.askopenfilename())) 

    outputEntry.grid(row=1, column=2)

    outputLabel = tk.Label(text="Input File")
    outputLabel.grid(row=1,column=1)



    outputFilename = tk.StringVar()
    outputFilename.set("freq.csv")
    if len(sys.argv) > 2:
        outputFilename.set(sys.argv[2])

    outputEntry = tk.Entry(textvariable=outputFilename)
    outputEntry.grid(row=2, column=2)

    outputLabel = tk.Label(text="Output File")
    outputLabel.grid(row=2,column=1)

    runButton = tk.Button(text="Create", command=main_program)
    runButton.grid(row=3,column=1)

    root.mainloop()
else:
    main_program()