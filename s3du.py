#!/usr/bin/python
#
# Copyright (c) 2015 Evgeny Gridasov (evgeny.gridasov@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import boto.s3;


def gib_size_str(bytes_size):
    return str( round(bytes_size / 1024.0 /1024/1024,2)) + " GiB"

def calculate_du(b, k, summary):
    standard = 0
    reduced = 0
    glacier = 0
    unknown = 0
    for key in b.list(prefix=k):
        if key.storage_class == "STANDARD":
            standard += key.size
        elif key.storage_class == "REDUCED_REDUNDANCY":
            reduced += key.size
        elif key.storage_class == "GLACIER":
            glacier += key.size + 32768 
            standard += 8192
        else:
            unknown += key.size
    
    s3path = "s3://" + b.name + "/" + k
    if summary:
        print (str(standard+reduced+glacier+unknown)) + "\t" + s3path 
    else:
        print s3path
        print "Standard Storage: " + str(standard) + "  (" + gib_size_str(standard) + ")" 
        print "Reduced Redundancy: " + str(reduced) + "  (" + gib_size_str(reduced) + ")"
        print "Glacier: " + str(glacier) + "  (" + gib_size_str(glacier) + ")"
        if unknown > 0: 
            print "Unknown: " + str(unknown)
        print ""



def recursive_du(conn, bucketname, keyname, summary, level):
    if level <= 0:
        return
    bucket = conn.get_bucket(bucketname)    
    for key in bucket.list(prefix=keyname, delimiter='/'):
        if key.name == keyname:
            continue
        if level == 1:
            calculate_du(conn.get_bucket(bucketname), key.name, summary)
        else:
            recursive_du(conn, bucketname, key.name, summary, level - 1)

# main entry
if __name__ == "__main__":

    try:
        import argparse 
    except ImportError:
        print "ERROR: You are running Python < 2.7. Please use pip to install argparse:   pip install argparse"


    parser = argparse.ArgumentParser(add_help=True, description="Print out S3 disk usage du by storage class")
    parser.add_argument("--max-depth", "-m", type=int, help="Maximum depth (0 by default)", default=0)
    parser.add_argument("--summary", "-s", action="store_true", help="Summary report only, without storage class details")
    parser.add_argument("s3url", type=str, help="S3 URL s3://bucketname/key")

    args = parser.parse_args()

    bucketname, keyname = "",""
    try: 
        s3url = args.s3url
        if s3url[0:5] != "s3://":
            raise
        _, path = s3url.split("s3://", 1)
        bucketname, keyname = path.split("/", 1)
    except:
        print "S3 URL should be in the form s3://bucketname/key or s3://bucketname/"
        quit(1)

    maxdepth = args.max_depth
    
    conn = boto.s3.connect_to_region("ap-southeast-2")
    if maxdepth == 0:
        bucket = conn.get_bucket(bucketname)
        calculate_du(bucket, keyname, args.summary)
    else:
        recursive_du(conn, bucketname, keyname, args.summary, maxdepth)
