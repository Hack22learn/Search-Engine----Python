#!/usr/bin/env python
import anydbm
'''
This program reads urls from crawled.db file and writes it to text file crawled.txt
'''
print "Used to coppy all urls of crawled list in text file crawled"
f=open('crawl.txt','w')
db=anydbm.open("crawled.db")
for key in db:
    f.write(key+'\n')

db.close()
f.close()
print 'we r done'
