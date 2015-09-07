from pymongo import MongoClient
import unirest
import csv


def sentiment_scores(db_name):
    client = MongoClient()
    db = client[db_name + '_db']
    collection = db[db_name + '_collection']
    posts = db['posts']

    senti_list = []
    count = 0
    f = open('%s_sentiments.csv' % db_name, 'wb')
    writer = csv.writer(f)
    writer.writerow(["id","time","sentiment","score"])
    for post in posts.find():
        message = ""
        time = ""
        id = ""

        if db_name == "blrcitypolice":
            if 'message' in post:
                message = post['message'] 
            elif 'description' in post:
                message = post['description']
            time = post['created_time']
            id = post['post_id']

        else:
            message = post['text']
            time = post['created_at']
            id = post['id_str']

        response = unirest.post("https://community-sentiment.p.mashape.com/text/",
            headers={
                "X-Mashape-Key": "gHgfU3fRkJmshJIkZHwr69Z9YLYIp1gcCE9jsnN6Y9fYrjk59R",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
                },
            params={
                "txt": message
                }
        )
        if response.code == 200:
            count += 1
            print count
            #print response.code
            #senti_list.append([id,time,response.body['result']['sentiment'],response.body['result']['confidence']])
            writer.writerow([id,time,response.body['result']['sentiment'],response.body['result']['confidence']])
        
        

    print count
    return senti_list

print sentiment_scores('blrcitypolice')[:10]