#!/usr/bin/env python
import sys,urllib2
def union_list(keyword,keys):
    '''
      take two list as input then take union of it
    '''
    for key in keys:
        if key not in keyword:
            keyword.append(key)
            

def index_page(url):
    '''
    index web page > extract keywords
    Till Now Our we extract only title,keyword,Description
     'we leave h1 and h2 tag'
    '''
    try:
        try:
            response=urllib2.urlopen(url)
            page_data=response.read()
        except:
            print 'unable to connect'
            sys.exit()
        
        keyword=[]
        # find data within head tag
        head=page_data.find("<head>")
        tail=page_data.find("</head>",head+1)
        head_data=page_data[head+6:tail]
        
        #find data within title and make it keyword
        title_h=head_data.find('<title')
        title_h=head_data.find('>',title_h)
        title_f=head_data.find('</title>',title_h)
        data=head_data[title_h+1:title_f]
        keys=data.split(' ') #list of keyword
        union_list(keyword,keys)
        del data,keys
        #print keyword
        
        
        meta_h=0
        while True:
            meta_h=head_data.find('<meta name',meta_h)
            temp=meta_h
            if meta_h ==-1:
                break
                
            meta_h=head_data.find('content',meta_h)
            if meta_h !=-1 and (head_data[temp:meta_h].find('keywords') !=-1 or head_data[temp:meta_h].find('description') !=-1):
                m_h=head_data.find('"',meta_h)
                meta_h=head_data.find('"',m_h+1)
                keys=head_data[m_h+1:meta_h].split(' ')
                union_list(keyword,keys)
                del keys,temp

        print keyword
        # Till Now Checked
       
        
    except KeyboardInterrupt:
        print 'Keyboard intrupt CTRL+C'
        sys.exit()
    
if __name__ == '__main__':
    url='''http://mondaymorning.nitrkl.ac.in/index.php/departments/2012-07-19-05-44-20/computer-science-and-engineering'''
    #url='''http://nitrkl.ac.in/Academic/1Department/Home.aspx?hsgf32njk=Mw%3d%3d-yoe1zDBzzaE'''
    index_page(url)
