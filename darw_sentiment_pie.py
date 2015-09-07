import csv
import matplotlib.pyplot as plt

def senti_pie(csv_name):
    f = open(csv_name + '_sentiments.csv','rb')
    reader = csv.reader(f)

    senti_list = list(reader)

    tot = len(senti_list)
    neutrals = 0
    positives = 0
    negatives = 0

    for lst in senti_list:
        if lst[2] == 'Neutral':
            neutrals += 1
        if lst[2] == 'Positive':
            positives += 1
        if lst[2] == 'Negative':
            negatives += 1

    labels = 'Neutral','Positive','Negative'
    sizes = [neutrals/(tot * 1.0) * 100, positives/(tot * 1.0) * 100, negatives/(tot * 1.0) * 100]
    explode=(0,0.05,0)

    plt.pie(sizes, explode=explode, labels=labels,
        autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('Sentiment distribution of ' + csv_name, bbox={'facecolor':'0.8', 'pad':5})

    #show()
    plt.savefig(csv_name+"_sentiment_dist.png",format="png", dpi=100)

#senti_pie('ponguru')
#senti_pie('blrcitypolice')
senti_pie('thekiranbedi')