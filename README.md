#PoET
## Overview
PoET is a command line tool for extracting data from the Path of Exile content package.

## Installation
PoET was developed against [Python 3.2.3](http://www.python.org/download/). As such, you require a Python 3.x interpreter to use it. PoET is simple to use. Here is an example:

    $ poet.py extract "path/to/Content.ggpk" "directory/to/extract/to"

You may pass -h to the script to receive more detailed help:

    $ poet.py -h
    usage: poet.py [-h] {extract,diff} ...
    
    Path of Exile Tool
    
    positional arguments:
      {extract,diff}
        extract       Extracts a .ggpk file
        diff          Provides a summary of whatchanged between two extraction
                      versions
    
    optional arguments:
      -h, --help      show this help message and exit

## License
[Apache License](http://www.apache.org/licenses/LICENSE-2.0.html)
