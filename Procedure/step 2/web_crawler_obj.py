#!/usr/bin/env python

import anydbm,sys,urllib2,time

class Web_Crawler(object):
    '''
       crawl all web-pages of nitrkl and other sites at NITR server
    '''
    
    def __init__(self):
        self.to_be_crawl=anydbm.open('To Be Crawl.db','c')
        self.crawled=anydbm.open('crawled.db','c')
        
    
    def do_not_crawl(self,link):
        '''
           This function tests if a link refers to img or css or anything not important for indexing
           it returns false else it returns true
        '''
        if link.find('nitrkl') !=-1:
            if link.find("#")!=-1 and link.find('(') == -1 and link.find(',') ==-1 and link.find("'") ==-1 and link.find('javascript') == -1:
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
    
    def link_create(self,cur_link,append_link):
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
        
    def crawl_page(self,url):
        '''
            Extract all links from a given url
        '''
        try:
            response=urllib2.urlopen(url)
            page_data=response.read()
            self.crawled[url]='' # insert url to crawled list
        except:
            return
            
        start_link=-1
        while True:
            '''
                 fetch all links , this loop continues until all links are extracted
            '''
            start_link=page_data.find("href=",start_link+1)
            if start_link == -1:
                break
            else:
                start_quote=page_data.find('"',start_link)
                end_quote=page_data.find('"',start_quote+1)
    
                Test_is_url=page_data[start_quote+1:end_quote]
                
                if (Test_is_url.find('http') !=-1): #cmake sure it is a url and distinct url
                    if self.do_not_crawl(Test_is_url) and Test_is_url not in self.to_be_crawl and Test_is_url not in self.crawled:
                        self.to_be_crawl[Test_is_url]=''
                    
                elif(Test_is_url.find('www.') != -1):
                    Test_is_url = 'http://'+Test_is_url
                    if self.do_not_crawl(Test_is_url) and Test_is_url not in self.to_be_crawl and Test_is_url not in self.crawled:
                        self.to_be_crawl[Test_is_url]=''
                        
                else:
                    addr=self.link_create(url,Test_is_url)
                    if self.do_not_crawl(addr) and addr not in self.to_be_crawl and addr not in self.crawled:
                        self.to_be_crawl[addr]=''
                        
            
    def start_iteration(self,seed=''):
        '''
           It Start web crawling
        '''
        try:
            if seed=='' and len(self.to_be_crawl)==0:
                self.to_be_crawl["http://nitrkl.ac.in"]=''
            elif seed!='' and len(self.to_be_crawl)==0:
                self.to_be_crawl[seed]=''
            
            count=-1
            start_time=time.clock()
            while(len(self.to_be_crawl)>0):
                keys=self.to_be_crawl.keys()
                for key in keys:
                    if count==50:
                        count=0
                        crwl_len=len(self.crawled)
                        print "To be crawl :",len(self.to_be_crawl),"::crawled :-",crwl_len,"Time stamp :",time.clock()-start_time,"sec"
                        if crwl_len >500:
                            self.crawled.close()
                            self.to_be_crawl.close()
                            sys.exit()
                            
                    count +=1
                    self.crawl_page(key)
                    del self.to_be_crawl[key]
            
            self.crawled.close()
            self.to_be_crawl.close()
            
        except KeyboardInterrupt:
            print 'you entered ctrl+c'
            sys.exit()
                
            
       
if __name__=='__main__':
    ob=Web_Crawler()
    ob.start_iteration("http://nitrkl.ac.in")
