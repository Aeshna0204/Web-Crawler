
from datetime import datetime
from datetime import timedelta


from pymongo import MongoClient
from cfg import config, db_cfg


client = MongoClient(db_cfg['host'], db_cfg['port'])


db = client[db_cfg['db']]

# print(myclient.list_database_names())
   
def insert_root(url):
    '''
    This function manually inserts the root url in the database
    '''
    doc = {
        'Link': url,
        'Source Link': url,
        'isCrawled':False,          #not crawled yet
        'Last Crawled': "Never",
        'Response Status':'' ,               
        'Content Type' :'',             
        'Content length': '',            
        'File Path':"",
        'Date Created': datetime.now()
    }
    db.linkcol.insert_one(doc)

def insert_new_links(new_urls, source_url, max_url):
    '''
    Inserts all the new links on a page in database
    source url is the link from which it was first extracted
    '''
    
    for link in new_urls:
        if(already_inserted(link)):
            continue        
        doc = {
            'Link': link,
            'Source Link': source_url,
            'isCrawled':False,      ##Initially the links are not crawled
            'Last Crawled': "Never",
            'Response Status':'' ,              
            'Content Type' :'',               
            'Content length': '',             
            'File Path':"",
            'Date Created': datetime.now()
        }
        if max_url<=db.linkcol.count_documents({}):
            break
        db.linkcol.insert_one(doc)   
        print(link+" inserted at "+str(db.linkcol.count_documents({})))


def already_inserted(link):
    '''
    checks if a link is already present in the database
    '''
    if db.linkcol.find_one({'Link':link})==None:
        return False
    return True


def all_crawled():
    '''
    This function check if there are uncrawled links which are
    1. If they are never crawled before or
    2. if they are crawled before 24 hours
    :return: count of all uncrawled links
    '''
    count=0
    for doc in db.linkcol.find({}):
        if doc['Last Crawled']!='Never':
            time_diff = datetime.now()-doc['Last Crawled']
            if time_diff.days>=config['time_diff']:
                count=count+1
        else:
            count=count+1
    return count

def get_all_uncrawled():
    uncrawled_url = set()
    for doc in db.linkcol.find({}):
        if doc['Last Crawled']=='Never':
            uncrawled_url.add(doc['Link'])
        else:
            time_diff = datetime.now()-doc['Last Crawled']
            if time_diff.days>=config['time_diff']:
                uncrawled_url.add(doc['Link'])
    return uncrawled_url 