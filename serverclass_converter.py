#!/usr/bin/env python

import argparse
import sys
import logging
import configparser
import re
import csv
import os

optarg = argparse.ArgumentParser(prog="serverclass_converter",description="Convert serverclass white/blacklist entries into CSV files.")
optarg.add_argument('-d','--debug',help="Enable debug logging.",action="store_const",const="yes")
optarg.add_argument('-f','--config',help="serverclass.conf configuration to process.")
optarg.add_argument('-a','--app',help="App name for serverclass.conf output lookup files. Defaults to app_serverclass.",default="app_serverclass")
config = optarg.parse_args()

if config.debug == "yes":
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG,stream=sys.stderr)
else:
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO,stream=sys.stderr)


# Create the config parser in case-sensitive mode
serverclass = configparser.RawConfigParser()
serverclass.optionxform = lambda option: option
logging.info("Reading in the serverclass.conf file...")
serverclass.read(config.config)

logging.debug("Creating app directories for output.")
try:
	os.makedirs(config.app + '/local', 0755)
	os.makedirs(config.app + '/lookups', 0755)
	os.makedirs(config.app + '/metadata', 0755)
except:
	logging.error("Unable to create app directories.")
	raise

localmeta = '''[]
access = read : [ * ], write : [ admin ]
export = system
'''

logging.debug("Creating local.meta file in metadata directory.")
with open(config.app + '/metadata/local.meta', 'w') as meta:
	meta.write(localmeta)
	meta.close()

logging.debug("Opening serverclass.conf file for output")
try:
	sc_file = open(config.app + '/local/serverclass.conf', 'w')
except:
	raise

scdefault = '''# Make the Forwarder Management GUI read-only so it does not clobber
# our CSV configurations
[default]
whitelist.0 = -

'''
logging.debug("Added read-only header to serverclass.conf")
sc_file.write(scdefault)

for stanza in serverclass:
	m = re.search('^serverClass:([^:]+)$',stanza)
	if m is None:
		logging.debug("{} is not a base serverClass definition.".format(stanza))
		continue
	base = m.group(1)

	logging.info("Found serverClass {}".format(base))

	logging.debug("Opening whitelist file for serverClass {}".format(base))
	try:
		whitelist_file = open(config.app + '/lookups/' + base + '.csv', 'w')
		whitelist = csv.writer(whitelist_file)
	except:
		logging.error("Failed to open whitelist file.")
		raise
	blacklist_file = None

	logging.debug("Writing out host header to whitelist file for serverClass {}".format(base))
	whitelist.writerow(['host'])

	wl_count = 0
	bl_count = 0

	while 'whitelist.'+str(wl_count) in serverclass[stanza]:
		logging.debug("Writing out attibute whitelist.{} for serverClass {}".format(wl_count,base))
		whitelist.writerow([serverclass[stanza]['whitelist.'+str(wl_count)]])
		wl_count += 1

	if not whitelist_file.closed:
		logging.debug("Closing whitelist file for serverClass {}".format(base))
		whitelist_file.close()

	sc_file.write("[{}]\n".format(stanza))
	sc_file.write("whitelist.from_pathname = etc/apps/{}/lookups/{}.csv\n".format(config.app,base))
	sc_file.write("whitelist.select_field = host\n")

	while 'blacklist.'+str(bl_count) in serverclass[stanza]:
		logging.debug("Writing out attibute blacklist.{} for serverClass {}".format(bl_count,base))
		if not blacklist_file:
			logging.debug("Opening blacklist file for serverClass {}".format(base))
			try:
				blacklist_file = open(config.app + '/lookups/' + base + '_blacklist.csv', 'w')
				blacklist = csv.writer(blacklist_file)
			except:
				logging.error("Failed to open blacklist file.")
				raise
			logging.debug("Writing out host header to blacklist file for serverClass {}".format(base))
			blacklist.writerow(['host'])

		blacklist.writerow([serverclass[stanza]['blacklist.'+str(bl_count)]])
		bl_count += 1

	if isinstance(blacklist_file,file) and not blacklist_file.closed:
		logging.debug("Writing out blacklist configuration")
		sc_file.write("blacklist.from_pathname = etc/apps/{}/lookups/{}_blacklist.csv\n".format(config.app,base))
		sc_file.write("blacklist.select_field = host\n")
		logging.debug("Closing blacklist file for serverClass {}".format(base))
		blacklist_file.close()

	sc_file.write("\n")

	for appstanza in serverclass:
		m = re.search('^' + stanza + ':app:(.*)$',appstanza)
		if m is None:
			logging.debug("{} is not an app in the serverClass {}.".format(appstanza,base))
			continue
		appbase = m.group(1)
		logging.debug("Writing out app definition for app {} in serverClass {}".format(appbase,base))
		sc_file.write("[" + appstanza + "]\n")
		for attr in serverclass[appstanza]:
			sc_file.write(attr + " = " + serverclass[appstanza][attr] + "\n")
		sc_file.write("\n")

	logging.info("Finished serverClass {}".format(base))

sc_file.close()
