from pymongo import MongoClient
import csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def word_cloud(db_name):
    client = MongoClient()
    db = client[db_name + '_db']
    collection = db[db_name + '_collection']
    posts = db['posts']

    all_tweets = ""
    count = 0
    for post in posts.find():
        message = ""
        #time = ""
        #id = ""

        if db_name == "blrcitypolice":
            if 'message' in post:
                message = post['message'] 
            if 'description' in post:
                message += " " + post['description']
            #time = post['created_time']
            #id = post['post_id']

        elif db_name == "cerc":
            if 'what' in post:
                message += post['what']
            if 'where' in post:
                message += " " + post['where']
            if 'when' in post:
                message += " " + post['when']

        else:
            message = post['text']
            #time = post['created_at']
            #id = post['id_str']
        
        all_tweets += message + "\n"

    #tags = make_tags(get_tag_counts(all_tweets), maxsize=120)
    print len(all_tweets)
    #create_tag_image(tags, db_name + '_cloud_large.png', size=(900, 600), fontname='Lobster')
    wordcloud = WordCloud().generate(all_tweets)
    # Open a plot of the generated image.
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(all_tweets)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(db_name+"_word_cloud_rel.png",format="png", dpi=100)


word_cloud("cerc")
#word_cloud("blrcitypolice")
#word_cloud("ponguru")
#word_cloud("thekiranbedi")