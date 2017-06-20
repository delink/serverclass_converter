#!/usr/bin/env python

import argparse
import sys
import logging
import configparser
import re
import csv

optarg = argparse.ArgumentParser(prog="serverclass_converter",description="Convert serverclass white/blacklist entries into CSV files.")
optarg.add_argument('-d','--debug',help="Enable debug logging.",action="store_const",const="yes")
optarg.add_argument('-f','--config',help="serverclass.conf configuration to process.")
config = optarg.parse_args()

if config.debug == "yes":
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG,stream=sys.stderr)
else:
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO,stream=sys.stderr)


serverclass = configparser.ConfigParser()

serverclass.read(config.config)

for stanza in serverclass:
	m = re.search('^serverClass:([^:]+)$',stanza)
	if m is None:
		logging.debug("{} is not a base serverClass definition.".format(stanza))
		continue
	base = m.group(1)

	logging.info("Found serverClass {}".format(base))

	logging.debug("Opening whitelist file for serverClass {}".format(base))
	try:
		whitelist_file = open(base + '.csv', 'w')
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

	while 'blacklist.'+str(bl_count) in serverclass[stanza]:
		logging.debug("Writing out attibute blacklist.{} for serverClass {}".format(bl_count,base))
		if not blacklist_file:
			logging.debug("Opening blacklist file for serverClass {}".format(base))
			try:
				blacklist_file = open(base + '_blacklist.csv', 'w')
				blacklist = csv.writer(blacklist_file)
			except:
				logging.error("Failed to open blacklist file.")
				raise
			logging.debug("Writing out host header to blacklist file for serverClass {}".format(base))
			blacklist.writerow(['host'])

		blacklist.writerow([serverclass[stanza]['blacklist.'+str(bl_count)]])
		bl_count += 1

	if isinstance(blacklist_file,file) and not blacklist_file.closed:
		logging.debug("Closing blacklist file for serverClass {}".format(base))
		blacklist_file.close()

	logging.info("Finished serverClass {}".format(base))
