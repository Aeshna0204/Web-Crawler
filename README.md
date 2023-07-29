# Web-Crawler
This Web Crawler recursively web Scraps all the links available on the given url and stores the meta data as well as the links in a MongoDB database.This crawler can be used to extract the information on any site by just entering the desired url.

### How to run the project?
To web scraps the links you need to run "web_crawler.py" file using below command:
```bash
python -u "d:\<your directory structure>\web Crawler\web_crawler.py"
```
All your scraped links get stored in current directory

### Database Configuration
You need to install MongoDB,MongoDB shell with any version(recommended latest version)
#### Connecting MongoDB to localhost using PyMongo
```bash
python
>>>from pymongo import MongoClient
>>> client=MongoClient['localhost',27017]
```
#### To create the CrawlerDB database run this command
```bash
mydb = client[‘name_of_the_database’]
```
### File Description
##### cfg.py 
Contains necessary configuration like max url size and hardcoded url to scrap etc
##### db_utils.py
Contains function that interact with the database and stores links to database
##### web_crawler.py
Main function ,handles all exceptions and crawles links from the site.
##### web_utils.py
Checks validity of url
