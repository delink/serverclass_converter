serverclass_converter.py
========================

Purpose
-------

I am converting a set of standard serverclass files into CSV-type files for
a customer. Creating all of those CSV files manually sounded awful, so here
we go.

Usage
-----

    usage: serverclass_converter [-h] [-d] [-f CONFIG]

    Convert serverclass white/blacklist entries into CSV files.

    optional arguments:
      -h, --help                    show this help message and exit
      -d, --debug                   Enable debug logging.
      -f CONFIG, --config CONFIG    serverclass.conf configuration to process.

Output
------

All of the CSV files will be output into the current directory. If you have
a stanza "[serverClass:ServerList]", you will end up with two CSV files:
ServerList.csv and ServerList_blacklist.csv. There will be a header row with
the field name "host". 

Caveats
-------

This program assumes you are feeding it a serverclass.conf that is valid for
use in the Forwarder Management GUI of Splunk. No funny stuff.
