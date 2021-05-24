# created by Shaun D Ramsey - 2021 
# version 05.24.21  - class singleton creation for use with log, log_open and log_close
#                   - this log_setup also controls the verbosity 
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


import datetime

def log(msg, level=1):
    logger = LogSingleton()

    if logger.VERBOSITY >= level:
        if level > 1:
            msgo = f' [{level}]: {msg}'
        elif level == 0:
            msgo = f" [ERROR]: {msg}"
        else:
            msgo = msg

    if logger.VERBOSITY >= level:
        print(msgo)
    if logger.LOGFILE:
        if logger.LOGFILE_OBJ:
            logger.LOGFILE_OBJ.write(f"[{level}]: {msg}\n")
        else:
            #log(" Something went wrong with the log file", 0)
                pass


def log_setup(filename = "log", verbosity = 1):
    log_obj = LogSingleton()
    log_obj.setup(filename, verbosity)
    dt_string = datetime.datetime.now().strftime("%H:%M:%S")
    log(f' ** RUN BEGINS @ {dt_string} **', 999)
    log(f' ** OPENING LOGFILE "{log_obj.FULL_FILENAME}"', 1)


def log_close():
    log_obj = LogSingleton()
    log(f' ** CLOSING LOGFILE "{log_obj.FULL_FILENAME}"', 1) 
    dt_string = datetime.datetime.now().strftime("%H:%M:%S")
    log(f' ** RUN ENDS @ {dt_string}\n', 999)
    log_obj.close()


class LogSingleton():
    LOGFILE_OBJ = None
    VERBOSITY = 1
    LOGFILE = False
    _instance = None
    FULL_FILENAME = None
    
    def close(self):
        if self.LOGFILE_OBJ:
            self.LOGFILE_OBJ.close()
        self.LOGFILE_OBJ = None
        self.LOGFILE = False
        self.FULL_FILENAME = None

    def setup(self, logfilename="log", verbosity=1):
            if self.LOGFILE_OBJ:
                log_close()
            self.LOGFILE = True
            today = datetime.date.today()
            day_month_year = today.strftime("%d%m%Y")
            self.VERBOSITY = verbosity
            self.FULL_FILENAME = logfilename + day_month_year + ".log"
            self.LOGFILE_OBJ = open(self.FULL_FILENAME, "a")

    

    def  __new__(cls):
        if cls._instance is None:
            print('**Created** - DEBUG - DELETE')
            cls._instance = super(LogSingleton, cls).__new__(cls)
        return cls._instance

    




