from pymongo import MongoClient
import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
from operator import itemgetter

def timeAndPosts(db_name, val, format):
    client = MongoClient()
    db = client[db_name + '_db']
    collection = db[db_name + '_collection']
    posts = db['posts']

    feeds = []
    date_freq = {}
    for post in posts.find():
        dt = None
        if 'created_time' in post:
            dt = DT.datetime.strptime(post['created_time'][:val], format)
            feeds.append(dt)

            if dt not in date_freq:
                date_freq[dt] = 1
            else:
                date_freq[dt] += 1

        if 'created_at' in post:
            dt =  DT.datetime.strptime((str(post['created_at'].year)+"-"+str(post['created_at'].month))[:val], format)
            feeds.append(dt)
            if dt not in date_freq:
                date_freq[dt] = 1
            else:
                date_freq[dt] += 1

    
    od = sorted(date_freq.iteritems(), key=itemgetter(0))[2:]
    x = [date2num(date) for (date, no_of_posts) in od]
    y = [no_of_posts for (date, no_of_posts) in od]

    print od
    fig = plt.figure()
    fig.set_size_inches(18.5,11)

    graph = fig.add_subplot(110)
    
    # Plot the data as a red line with round markers
    graph.plot(x,y,'g-o')
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.xticks(rotation='vertical')
    plt.ylabel('Number of posts')
    plt.xlabel('Time')
    plt.title('Number of posts VS Time')
    for i,j in zip(x,y):
        graph.annotate('%s' %j, xy=(i,j), xytext=(5,5), textcoords='offset points')
        #graph.annotate('(%s,' %i, xy=(i,j))
    axes = plt.gca()
    axes.set_ylim([0,max(y)+max(y)/5])
    # Set the xtick locations to correspond to just the dates you entered.
    graph.set_xticks(x)

    # Set the xtick labels to correspond to just the dates you entered.
    graph.set_xticklabels([date.strftime(format) for (date, value) in od])
    #plt.grid(True)
    plt.savefig(db_name+"_year.png",format="png", dpi=200)

timeAndPosts('cerc',7,"%Y-%m")
timeAndPosts('blrcitypolice',7,'%Y-%m')
timeAndPosts('ponguru',7,'%Y-%m')
timeAndPosts('thekiranbedi',7,'%Y-%m')