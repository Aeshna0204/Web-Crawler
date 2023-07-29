from cfg import config, db_cfg
from db_utils import insert_root, insert_new_links
from db_utils import all_crawled, get_all_uncrawled
from web_utils import get_all_links


from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed


from datetime import datetime, timedelta
import time
import random
import string
import os


import requests
import warnings
warnings.filterwarnings("ignore")


client = MongoClient(db_cfg['host'], db_cfg['port'])

client.list_database_names()

db = client[db_cfg['db']]

url=config['root url']

insert_root(url)

def crawler_engine(url,max_url):
    try:
        extension = (requests.get(url).headers['Content-Type'].split('/')[-1].split(';')[0])
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        file_name = (result_str+'.'+extension)
        content = requests.get(url).text
                
        with open(file_name,'wb') as f:
            f.write(content.encode())
                    
        cwd = os.getcwd()     
        file_path = os.path.join('D:\Tashu New\Aeshna -1 mock interview\web crwaler\Links',file_name)    
                
        db.linkcol.update_one({'Link':url}, {'$set':
                                            {'isCrawled':True, 'Last Crawled':datetime.now(),
                                            'Response Status':requests.get(url).status_code,
                                            'Content Type':requests.get(url).headers['Content-Type'],
                                            'Content length':len(requests.get(url).content),
                                            'File Path':file_path}})
        if(max_url<=db.linkcol.count_documents({})):
            return "Maximum Limit Reached"
        new_links = get_all_links(url)    
        insert_new_links(new_links, url, max_url)
            
    except requests.exceptions.SSLError:
        db.linkcol.update_one({'Link':url}, {'$set':
                                            {'isCrawled':True, 'Last Crawled':datetime.now()}})
    except requests.exceptions.ConnectionError:
        db.linkcol.update_one({'Link':url}, {'$set':
                                            {'isCrawled':False, 'Last Crawled':datetime.now()}})
    except requests.exceptions.Timeout:
        db.linkcol.update_one({'Link':url}, {'$set':
                                            {'isCrawled':False, 'Last Crawled':datetime.now()}})
    except requests.exceptions.HTTPError:
        db.linkcol.update_one({'Link':url}, {'$set':
                                            {'isCrawled':False, 'Last Crawled':datetime.now()}})
    return ""    

def crawl(max_url=config['max_url']):
    if(all_crawled()==0):
        print("All Links Crawled")
    else:    
        uncrawled_urls = get_all_uncrawled()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for url in uncrawled_urls:
                futures.append(executor.submit(crawler_engine, url,max_url))
            for future in as_completed(futures):
                print(future.result())
    
    time.sleep(config['sleep_time'])        
    crawl(max_url)

crawl()
