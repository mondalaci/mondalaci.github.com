#!/usr/bin/env python

import sys;
import os;
import codecs;

utf8_decoder = None
decoder = None
encoder = None

def rename_if_needed (dirname, f):
    try:
        utf8_decoder (f, "strict")
    except UnicodeError:
        try:
            d = decoder (f, "strict")
            try:
                c = encoder (d[0], "strict")
                if (c[0] != f):
		    srcfile = os.path.join(dirname, f)
		    if not os.access(srcfile, os.W_OK):
			print "Cannot rename file '%s' because it is not writable" % (srcfile)
			return
			
                    print "Renaming " + os.path.join (dirname, f) + " to " + os.path.join (dirname, c[0])
                    os.rename (os.path.join (dirname, f),
                               os.path.join (dirname, c[0]))
            except UnicodeError:
                print "You are totally fucked with file " + os.path.join (dirname, f)
                sys.exit (1);

        except UnicodeError:
            print "File " + os.path.join (dirname, f) + " not in the encoding you specified; skipping"

def fix_dir (dirname):
    dirs = []
    files = []

    if not os.access(dirname, os.R_OK):
	print "Directory '%s' is not readable" % (dirname)
	return

    for f in os.listdir (dirname):
	fullpath = os.path.join(dirname, f)
        if os.path.isdir (fullpath):
            dirs.append (f);
        else:
            files.append (f);

    for f in files:
        rename_if_needed (dirname, f)

    for d in dirs:
        fix_dir (os.path.join (dirname, d))
        rename_if_needed (dirname, d)

if len (sys.argv) < 2:
    sys.stderr.write ("Converts filenames to UTF-8 encoding, recursively\n"
                      "\n"
                      "Usage: fix-filenames.py <ORIGINAL_CHARSET>\n"
                      "\n"
                      "Example: fix-filenames.py ISO8859-1\n");
    sys.exit (1);

old_encoding = sys.argv[1]

utf8_decoder = codecs.getdecoder ("utf-8")
decoder = codecs.getdecoder (old_encoding)
encoder = codecs.getencoder ("utf-8")

fix_dir (os.getcwd ())
