import pymongo
from scrapers.region_scraper import get_all_regions

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["test_db"]
mycol = mydb["test_region"]

get_all_regions(mycol)