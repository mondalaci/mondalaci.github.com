#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

import sys
import os.path

argv = sys.argv
argnum = len(argv)

def print_help():
    print 'Usage: spacify INPUTFILE'
    print 'Converts tabs to spaces in files.'
    print 'Copyleft (C) 2005 Laszlo Monda <http://mondalaci.objecis.net>'
    sys.exit(1)

def process(input_filename):
    print "Processing " + input_filename + ':',
    if not os.path.isfile(input_filename):
	print 'invalid file: %s' % input_filename
	return

    tmp_filename = 'spacify.tmp'
    infile = open(input_filename)
    outfile = file(tmp_filename, 'w')

    for line in infile:
	ws_count = 0
	idx = 0
	char = line[idx]

        while (char==' ' or char=='\t'):
	    if (char == ' '):
    	        ws_count += 1
    	    elif (char == '\t'):
        	tabspace = ws_count % 4
        	remainder = 4 - tabspace
            
        	if remainder == 0:
            	    ws_count += 8
        	else:
            	    ws_count += remainder

    	    idx += 1
    	    char = line[idx]
        
	outfile.write(' ' * ws_count)
	outfile.write(line[idx:])

    outfile.close()
    os.rename(tmp_filename, input_filename)
    print 'OK'
if argnum == 1 or argnum == 2 and argv[1] == '-h' or argv[1] == '--help':
    print_help()

for filename in sys.argv[1:]:
    process(filename)

    