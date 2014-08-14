#!/usr/bin/env python
import anydbm
'''
This program read url from crawled.db file and write it to text file crawled.txt
'''
print "Used to coppy all url of crawled list in test file crawled"
f=open('crawl.txt','w')
db=anydbm.open("crawled.db")
for key in db:
    f.write(key+'\n')

db.close()
f.close()
print 'we r done'