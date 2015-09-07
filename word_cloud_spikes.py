from pymongo import MongoClient
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import datetime as DT


def word_cloud(db_name, dates):
    client = MongoClient()
    db = client[db_name + '_db']
    collection = db[db_name + '_collection']
    posts = db['posts']

    count = 0
    for date in dates:
        all_tweets = ""
        for post in posts.find():
            message = ""
            #time = ""
            #id = ""

            dt = ""
            if 'created_time' in post:
                dt = post['created_time'][:7]
            elif 'created_at' in post:
                dt = str(post['created_at'].year)+"-"
                temp = str(post['created_at'].month)
                if len(temp) == 1:
                    dt += "0"+temp
                else:
                    dt += temp
                #print dt
            if dt == date:
                if db_name == "blrcitypolice":
                    if 'message' in post:
                        message = post['message'].encode("ascii","ignore")
                    if 'description' in post:
                        message += " " + post['description'].encode("ascii","ignore")

                elif db_name == "cerc":
                    if 'what' in post:
                        message += post['what'].encode("ascii","ignore")
                    if 'where' in post:
                        message += " " + post['where'].encode("ascii","ignore")
                    if 'when' in post:
                        message += " " + post['when'].encode("ascii","ignore")

                else:
                    message = post['text']
            
                all_tweets += message + "\n"

        all_tweets =  all_tweets.encode("ascii","ignore")

        fout = open(db_name+"_"+date+".result","w")
        fout.write(all_tweets)
        fout.close()
        # take relative word frequencies into account, lower max_font_size
        wordcloud = WordCloud(max_font_size=40).generate(all_tweets)
        plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig(db_name+date+"_word_cloud_rel.png",format="png", dpi=100,bbox_inches='tight')


word_cloud("cerc",["2014-05","2014-11","2015-03","2015-06"])
word_cloud("blrcitypolice",["2012-08","2015-01","2015-03","2015-08"])
word_cloud("ponguru",["2011-04","2013-03","2014-02","2015-07"])
word_cloud("thekiranbedi",["2014-11","2015-05","2015-07","2015-08"])