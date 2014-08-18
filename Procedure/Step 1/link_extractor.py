#!/usr/bin/env python
import urllib2,sys

#Extracting All Distinct Links from Given Page!!

def do_not_crawl(link):
    '''
       This function tests if a link refers to img or css or anything not important for indexing
       it returns false else it returns true
    '''
    if link.find('nitrkl') !=-1 or link.find('192.168')!=-1:
        if link.find('(') == -1 and link.find(',') ==-1 and link.find("'") ==-1 and link.find('javascript') == -1:
            temp=link[-6:]
            pos=temp.find('.')
            temp=temp[pos+1:]
            if temp in ['css','js','img','pdf','ico']:
                return False
            else:
                return True
        else:
            return False
    else:
        return False

def link_create(cur_link,append_link):
    '''
      for shortened links like href="test.html"
      it returns full link required to fetch that page
    '''
    if append_link[0] not in './':
        return cur_link+'/'+append_link
    elif append_link[0] == '/':
        return cur_link+append_link
    elif append_link[0]=='.':
        back_url=0
        while True:
            if append_link.find('../')!=-1:
                back_url +=1
                append_link=append_link[3:]
            else:
                break
        try:
            count=0
            for j in range(len(cur_link)-1,-1,-1):
                if count == back_url+1:
                    cur_link=cur_link[:i+2]
                    break
                elif cur_link[i]=='/':
                    count +=1
            return cur_link+append_link
        except:
            return append_link
                    
    else:
        return append_link
        
          
def collect_all_link(page_data,cur_link):
    '''
      collect all valid urls from a web page
    '''
    url=[]
    start_link=-1
    while True:
        '''
           this loop is continued until all links are extracted i.e. no links are
           left in the page
        '''
        start_link=page_data.find("href=",start_link+1)
        if start_link == -1:
            break
        else:
            start_quote=page_data.find('"',start_link)
            end_quote=page_data.find('"',start_quote+1)

            Test_is_url=page_data[start_quote+1:end_quote]
            
            if (Test_is_url.find('http') !=-1): #cmake sure it is a url and distinct url
                if do_not_crawl(Test_is_url) and Test_is_url not in url:
                    url.append(Test_is_url)
                
            elif(Test_is_url.find('www.') != -1):
                Test_is_url = 'http://'+Test_is_url
                if do_not_crawl(Test_is_url) and Test_is_url not in url:
                    url.append(Test_is_url)
                    
            else:
                addr=link_create(cur_link,Test_is_url)
                if do_not_crawl(addr) and addr not in url :
                    url.append(addr)
                
        
    return url

if __name__=='__main__':
    
    try:
        addr='http://nitrkl.ac.in'
        response=urllib2.urlopen(addr)
        page_data=response.read()
    except:
        print 'Unable to fetch url'
        raw_input()
        sys.exit()
        
    url=collect_all_link(page_data,addr)
    for i in url:
        print i
    print 'No of element :-',len(url)
    raw_input()
