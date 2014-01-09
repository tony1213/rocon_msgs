#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_multimaster/license/LICENSE
#

##############################################################################
# Imports
##############################################################################

import sys
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import re
import os, os.path
import errno
import argparse

IODELIM   = '---'
AUTOGEN="# ====== DO NOT MODIFY! AUTOGENERATED FROM A SERVICE PAIR DEFINITION ======\n"

class PairSpecException(Exception): pass

def parse_service_pair_spec(text, package_context = ''):
    pieces = [StringIO()]
    for l in text.split('\n'):
        if l.startswith(IODELIM):
            pieces.append(StringIO())
        else:
            pieces[-1].write(l + '\n')
    return [p.getvalue() for p in pieces]

def write_file(filename, text):
    f = open(filename, 'w')
    f.write(text)
    f.close()

def main():

    parser = argparse.ArgumentParser(description='Service pair generator.')
    parser.add_argument('filename', nargs=1, type=str, help="filename of the .pair service")
    parser.add_argument('-o', '--output-dir', action='store', default='.', help='output directory')
    args = parser.parse_args()

    # Try to make the directory, but silently continue if it already exists
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise

    service_pair_file = args.filename[0]
    if not service_pair_file.endswith('.pair'):
        print("The file specified has the wrong extension. It must end in .pair")
    else:
        filename = service_pair_file

        f = open(filename)
        service_pair_spec = f.read()
        f.close()

        name = os.path.basename(filename)[:-7]
        (name, unused_sep, unused_ext) = os.path.basename(filename).partition('.')
        print("Generating for pair %s" % name)

        pieces = parse_service_pair_spec(service_pair_spec)
        if len(pieces) != 2:
            raise ActionSpecException("%s: wrong number of pieces, %d"%(filename,len(pieces)))
        service_request, service_response = pieces
        service_request_msg = AUTOGEN + service_request
        service_response_msg = AUTOGEN + service_response

        write_file(os.path.join(args.output_dir, "%sRequest.msg"%name), service_request_msg)
        write_file(os.path.join(args.output_dir, "%sResponse.msg"%name), service_response_msg)


if __name__ == '__main__': main()