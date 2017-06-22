serverclass_converter.py
========================

Purpose
-------

I am converting a set of standard serverclass files into CSV-type files for
a customer. Creating all of those CSV files manually sounded awful, so this
will do all of the tedious work for me.

Usage
-----

    usage: serverclass_converter [-h] [-d] [-f CONFIG] [-s] [-a APP]
    
    Convert serverclass white/blacklist entries into CSV files.
    
    optional arguments:
      -h, --help                    show this help message and exit
      -d, --debug                   Enable debug logging.
      -f CONFIG, --config CONFIG    serverclass.conf configuration to process.
      -a APP, --app APP             App name for serverclass.conf output lookup files.
                                    Defaults to app_serverclass.
Output
------

A valid Splunk app will be created in the current directory. It will be named
after the --app option value. If you have a stanza "[serverClass:ServerList]",
you will end up with two CSV files: ServerList.csv and ServerList_blacklist.csv.
There will be a header row with the field name "host". 

A serverclass.conf file will be created in local with the following content. The
app name is the same as what is used to create the current app directory.

    [serverClass:ServerList]
    whitelist.from_pathname = etc/apps/app_serverclass/lookups/ServerList.csv
    whitelist.select_field = host
    blacklist.from_pathname = etc/apps/app_serverclass/lookups/ServerList_blacklist.csv
    blacklist.select_field = host

Caveats
-------

This program assumes you are feeding it a serverclass.conf that is valid for
use in the Forwarder Management GUI of Splunk. No funny stuff.
