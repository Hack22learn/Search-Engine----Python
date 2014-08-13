#!/usr/bin/env python
import urllib2,sys
import time
#Extracting All Distinct Links, of nitrkl or its associate from web !!

def do_not_crawl(link):
    '''
       This function used to test this is not url for any download or image or anything we donot
       want to index by testing its end extention .i.e .img,.pdf,.css,.js
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
      for link like href="test.html"
      it create whole link to fetch that url
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
        
        
def connect_to_link(link):
    '''
      connect to given url and store data of that page in a variable
      then return that var
    '''
    try:
        response=urllib2.urlopen(link)
        page_data=response.read()
        return page_data
    except:
        return False
    
def collect_all_link(url,crawled):
    '''
      collect all valid url from web page
      and make sure it belong to nitrkl and it is not a download link
    '''
    #file handle
    f=open("url.txt",'w')
    o=open("crawled.txt",'w')
    utf=open("unable to fetch.txt",'w')
    #####################
    start_time=time.clock()
    count =0
    while True:
        count +=1
        if count ==100:
            print len(crawled),' time : ',time.clock()-start_time
            count=0
        cur_link =url[0]
        page_data = connect_to_link(cur_link)
        if page_data != False:
            o.write(cur_link+"\n")
            start_link=-1
            while True:
                '''
                 fetch all link :> this loop is continued until all link of given webpage extracted
                '''
                start_link=page_data.find("href=",start_link+1)
                if start_link == -1:
                    break
                else:
                    start_quote=page_data.find('"',start_link)
                    end_quote=page_data.find('"',start_quote+1)
                
                    Test_is_url=page_data[start_quote+1:end_quote]
                    
                    if (Test_is_url.find('http') !=-1): #cmake sure it is url and distinct url
                        if do_not_crawl(Test_is_url) and Test_is_url not in url and Test_is_url not in crawled:
                            url.append(Test_is_url)
                            f.write(Test_is_url+'\n')
                
                    elif(Test_is_url.find('www.') != -1):
                        Test_is_url = 'http://'+Test_is_url
                        if do_not_crawl(Test_is_url) and Test_is_url not in url and Test_is_url not in crawled:
                            url.append(Test_is_url)
                            f.write(Test_is_url+'\n')
                            
                    else:
                        addr=link_create(cur_link,Test_is_url)
                        if do_not_crawl(addr) and addr not in url and Test_is_url not in crawled:
                            url.append(addr)
                            f.write(addr+'\n')
                            
            
        else:
            utf.write(cur_link+'\n')
        
        del url[0] # delete fetch url from url list
        crawled.append(cur_link)
        
    f.close()
    o.close()
    utf.close()
    
        
if __name__=='__main__':
    
    try:
       url=['http://nitrkl.ac.in'] # url going to crawl
       crawled=[]  # URL already crawled
       collect_all_link(url,crawled)
       #collect_all_link(page_data,addr)
    except KeyboardInterrupt:
        print 'you press ctrl+c'
        sys.exit()
        
        
    print 'No of element :-',len(url)
    print 'Thanks bro!!'
    raw_input()
