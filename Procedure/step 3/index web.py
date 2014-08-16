#!/usr/bin/env python
import urllib2,sys
'''
   Crawl A index Page and extract all keyword for it ..
'''
def union_list(keyword,keys):
    '''
      take two list as input then take union of it
    '''
    for key in keys:
        if key not in keyword:
            keyword.append(key)
    print keyword        
def key_from_h12(page_data,h):
    '''
      return list of keyword
    '''
    keys=[]
    heading=0
    while True:
        heading=page_data.find(h,heading)
        if heading ==-1:
            break
       
        heading=page_data.find('>',heading)
        tail=page_data.find('</'+h+'>')
        key=page_data[heading+1:tail].split(' ')
        union_list(keys,key)
        heading=tail
        
    return keys
    
def index_page(url):
    '''
      extract keyword from page and return list of keyword
    '''
    try:
        try:
            response=urllib2.urlopen(url)
            page_data=response.read()
        except:
            print 'unable to connect'
            sys.exit()
        # find data within head tag
        head=page_data.find("<head>")
        tail=page_data.find("</head>",head+1)
        head_data=page_data[head+6:tail]
        
        #find data within title and make it keyword
        title_h=head_data.find('<title')
        title_h=head_data.find('>',title_h)
        title_f=head_data.find('</title>',title_h)
        data=head_data[title_h+1:title_f]
        keyword=data.split(' ') #list of keyword
        del data
        #find keyword in description
        meta_h=0
        while True:
            meta_h=head_data.find('<meta name',meta_h)
            if meta_h ==-1:
                break
            meta_h=meta_h.find('content',meta_h)
            if meta_h !=-1:
                m_h=meta_h.find('"',meta_h)
                meta_h=meta_h.find('"',m_h+1)
                keys=head_data[m_h+1:meta_h].split(' ')
                union_list(keyword,keys)
                del keys
        # make data within h1 and h2 as keyword
        del head_data
        page_data=page_data[tail+6:]
        keys=key_from_h12(page_data,'h1')
        union_list(keyword,keys)
        keys=key_from_h12(page_data,'h2')
        union_list(keyword,keys)
        del keys
        return keyword        
    except KeyboardInterrupt:
        print 'keyboard Intrupt'
        
if __name__ == '__main__':
    keys=index_page("http://nitrkl.ac.in")
    for key in keys:
        print key