import requests
import re
from pymongo import MongoClient
import csv


def remove_chars_re(subj, chars):
    return re.sub('[' + re.escape(''.join(chars)) + ']', '', subj)


client = MongoClient()
#client.database_names() shows databases names

cerc_db = client['cerc_db']
cerc_colle = cerc_db['cerc_collection']
posts = cerc_db['posts']


fin = open("fb-data.list", "r")
fout = open("five-w.csv", "w")

f = open('cercwww.csv','wb')
writer = csv.writer(f)
writer.writerow(["created_time","what","when","where"])

t = 1
while t:
    url = fin.readline()[:-1]
    ACCESS_TOKEN = fin.readline()[:-1]
    VERSION = fin.readline()[:-1]
    LIMIT = fin.readline()[:-1]
    ID = fin.readline()[:-1]
    fin.readline()[:-1]

    out = ""

    tot_url = url+VERSION+"/"+ID+"?access_token="+ACCESS_TOKEN+"&limit="+LIMIT

    #print tot_url

    response = requests.get(tot_url)

    feeds = response.json()
    print feeds
    count = 0
    while 'data' in feeds and len(feeds['data']) != 0:
        feeds_in_this_page = len(feeds['data'])
        for i in range(feeds_in_this_page):
            if 'description' in feeds['data'][i]:
                description = feeds['data'][i]['description']
                description = description.encode('ascii',  'ignore')
                name = feeds['data'][i]['name'].encode('ascii', 'ignore')

                what_pos = description.find("WHAT:")
                what_ends = description[what_pos + 5:].find(":")
                what_cont = description[what_pos:what_pos + 5 +what_ends - (description[what_pos:what_pos + 5 +what_ends])[::-1].find("\n")]
                what_cont = remove_chars_re(what_cont, ['\n', '+'])

                when_pos = description.find("WHEN:")
                when_ends = description[when_pos + 5:].find(":")
                when_cont = description[when_pos:when_pos + 5 +when_ends - (description[when_pos:when_pos + 5 +when_ends])[::-1].find("\n")]
                when_cont = remove_chars_re(when_cont, ['\n', '+'])

                where_pos = description.find("WHERE:")
                where_ends = description[where_pos + 6:].find(":")
                where_cont = description[where_pos:where_pos + 6 +where_ends - (description[where_pos:where_pos + 6 +where_ends])[::-1].find("\n")]
                where_cont = remove_chars_re(where_cont, ['\n', '+'])

                if len(what_cont) > 1 or len(where_cont) > 1 or len(when_cont) > 1 or name:
                    #print feeds['data'][i]['id'],"\n",feeds['data'][i]['created_time'],"\n",what_cont,"\n",when_cont,"\n",where_cont,"\n",name,"\n"                    
                    #post_id = posts.insert_one({'feed_id':feeds['data'][i]['id'],'created_time':feeds['data'][i]['created_time'],'what':what_cont[4:],'when':when_cont[4:],'where':where_cont[5:],'name':name})
                    #print post_id
                    writer.writerow([feeds['data'][i]['created_time'],what_cont.replace(",","")[6:],when_cont.replace(",","")[6:],where_cont.replace(",","")[7:]])
                    count += 1
                #break


        tot_url = feeds['paging']['next']
        response = requests.get(tot_url)
        feeds = response.json()
        #break
    print count
    #print feeds
    break
    t -= 1

