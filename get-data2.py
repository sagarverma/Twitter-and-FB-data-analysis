import requests
import re
from pymongo import MongoClient


def remove_chars_re(subj, chars):
    return re.sub('[' + re.escape(''.join(chars)) + ']', '', subj)


client = MongoClient()
#client.database_names() shows databases names

blrcitypolice_db = client['blrcitypolice_db']
blrcitypolice_colle = blrcitypolice_db['blrcitypolice_collection']
posts = blrcitypolice_db['posts']


fin = open("fb-data.list", "r")
fout = open("five-w.csv", "w")


url = fin.readline()[:-1]
ACCESS_TOKEN = fin.readline()[:-1]
VERSION = fin.readline()[:-1]
LIMIT = fin.readline()
ID = fin.readline()[:-1]

out = ""

tot_url = url+VERSION+"/"+ID+"?access_token="+ACCESS_TOKEN+"&limit="+LIMIT

#print tot_url

response = requests.get(tot_url)

feeds = response.json()
#print feeds
count = 0
while 'data' in feeds and len(feeds['data']) != 0:
    feeds_in_this_page = len(feeds['data'])
    for i in range(feeds_in_this_page):
            id = ""
            message = ""
            created_time = ""
            from_name = ""
            to_name = ""
            description = ""

            id = feeds['data'][i]['id']
            if 'message' in feeds['data'][i]:
                message = feeds['data'][i]['message']
            if 'description' in feeds['data'][i]:
                description = feeds['data'][i]['description']      
            created_time = feeds['data'][i]['created_time']
            from_name = feeds['data'][i]['from']['name']
            if 'to' in feeds['data'][i]:
                to_name = feeds['data'][i]['to']['data'][0]['name']

            print id

            post_id = posts.insert_one({'post_id': id,'message':message,'created_time':created_time,'from_name':from_name,'to_name':to_name,'description':description})
            print post_id
            count += 1

    tot_url = feeds['paging']['next']
    response = requests.get(tot_url)
    feeds = response.json()

print count
#print feeds
