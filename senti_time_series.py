import csv
import datetime as DT
import matplotlib.pyplot as plt
from operator import itemgetter
from matplotlib.dates import date2num
import numpy as np

def sign(senti):
    if senti == "Neutral":
        return 0
    if senti == "Negative":
        return -1
    if senti == "Positive":
        return 1

def senti_time_series(csv_name, val, format):
    f = open(csv_name + '_sentiments.csv','rb')
    reader = csv.reader(f)

    senti_list = list(reader)[1:]

    i = 0


    date_freq = {}

    for lst in senti_list:
        #print lst[1]
        dt = DT.datetime.strptime(lst[1][:val], format)
    
        #if i == 30:
        if dt not in date_freq:
            date_freq[dt] = [sign(lst[2])*float(lst[3])/100.0,1]
            #print dt
        else:
            #print dt
            date_freq[dt][0] += sign(lst[2])*float(lst[3])/100.0
            date_freq[dt][1] += 1
        i = 0
        #elif i < 30:
        i += 1

    
    od = sorted(date_freq.iteritems(), key=itemgetter(0))[:]
    x = [date2num(date) for (date, pair) in od]
    y = [pair[0]/pair[1] for (date, pair) in od]

    
    xrng = np.arange(0.0, 1.1, 0.01)

    fig = plt.figure(1)
    fig.set_size_inches(20,20)

    graph = fig.add_subplot(211)
    
    # Plot the data as a red line with round markers
    graph.plot(x,y,'b-o')
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.xticks(rotation='vertical')
    plt.ylabel('Sentiment Score')
    plt.xlabel('Time')
    plt.title('Sentiment Score VS Time')
    #for i,j in zip(x,y):
        #graph.annotate('%s' %j, xy=(i,j), xytext=(5,5), textcoords='offset points')
        #graph.annotate('(%s,' %i, xy=(i,j))
    axes = plt.gca()
    axes.set_ylim([-1.0,1.0])
    # Set the xtick locations to correspond to just the dates you entered.
    graph.set_xticks(x)

    # Set the xtick labels to correspond to just the dates you entered.
    graph.set_xticklabels([date.strftime(format) for (date, value) in od])
    #plt.grid(True)
    plt.savefig(csv_name+"_senti_time.png",format="png", dpi=200)

#senti_time_series('blrcitypolice',10,'%Y-%m-%d')
#senti_time_series('ponguru',10,'%Y-%m-%d')
senti_time_series('thekiranbedi',7,'%Y-%m')