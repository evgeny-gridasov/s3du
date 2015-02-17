s3du - Amazon S3 disk usage utility
===================================

Written by Evgeny Gridasov

http://egreex.com

https://awsreport.egreex.com

A quick du - like utility for Amazon S3 written in Python using boto.
Prints out S3 usage by storage class.

Examples
```
$ ./s3du.py s3://my-bucket/cool-stuff/music
s3://my-bucket/cool-stuff/music/
Standard Storage: 6603471360  (6.15 GiB)
Reduced Redundancy: 0  (0.0 GiB)
Glacier: 19404514832  (18.07 GiB)


$ ./s3du.py --max-depth=1 -s s3://my-bucket/cool-stuff/
26007986192	s3://my-bucket/cool-stuff/music/
20037957120	s3://my-bucket/cool-stuff/pictures/
350180736512	s3://my-bucket/cool-stuff/videos/
4961298432	s3://my-bucket/cool-stuff/documents/


$ ./s3du.py --max-depth=1 s3://my-bucket/cool-stuff/
s3://my-bucket/cool-stuff/music/
Standard Storage: 6603471360  (6.15 GiB)
Reduced Redundancy: 0  (0.0 GiB)
Glacier: 19404514832  (18.07 GiB)

s3://my-bucket/cool-stuff/pictures/
Standard Storage: 15546661376  (14.48 GiB)
Reduced Redundancy: 0  (0.0 GiB)
Glacier: 4491295744  (4.18 GiB)

s3://my-bucket/cool-stuff/videos/
Standard Storage: 54064509952  (50.35 GiB)
Reduced Redundancy: 0  (0.0 GiB)
Glacier: 296116226560  (275.78 GiB)

s3://my-bucket/cool-stuff/documents/
Standard Storage: 2298698752  (2.14 GiB)
Reduced Redundancy: 0  (0.0 GiB)
Glacier: 2662599680  (2.48 GiB)


```
