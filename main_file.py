from apiclient.discovery import build
from comment_threads import get_comment_threads
from search import youtube_search


import nltk
from nltk.corpus import stopwords
from nltk.corpus import movie_reviews
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.metrics import precision
from nltk.metrics import recall
from nltk.metrics import f_measure
import collections
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import PlaintextCorpusReader
corpus_pathpos  = 'C:/Users/User/Downloads/NLP Project Files/project/project/polarity/pos'
corpus_pathneg  = 'C:/Users/User/Downloads/NLP Project Files/project/project/polarity/neg'
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy

from collections import Counter

stopfile='english'
######################
pos_wordlist = PlaintextCorpusReader(corpus_pathpos,'.*')
neg_wordlist = PlaintextCorpusReader(corpus_pathneg,'.*')
positive_reviews = []
negative_reviews = []

for id in pos_wordlist.fileids():
    a =[str(word) for word in pos_wordlist.words(id)]
    positive_reviews.append(' '.join(a))

for id in neg_wordlist.fileids():
    a =[str(word) for word in neg_wordlist.words(id)]
    negative_reviews.append(' '.join(a))


# arguments to be passed to build function
DEVELOPER_KEY = "************************"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

negids=movie_reviews.fileids('neg')
posids=movie_reviews.fileids('pos')




def bag_of_words1(words):
    x = dict([(word, True) for word in words])
    return x

def bag_of_words(words):
    return dict([(word, True) for word in words])

N=10
ind=10
width=0.35
flag = 1;
i = 0
result = []
commentEncoded = []
if __name__ == "__main__":
    negfeats=[(bag_of_words(movie_reviews.words(fileids=[f])),'neg') for f in negids]
    posfeats=[(bag_of_words(movie_reviews.words(fileids=[f])),'pos') for f in posids]
    totalneg=len(negfeats)
    totalpos=len(posfeats)
    trainfeats=negfeats[:totalneg]+posfeats[:totalpos]
    badwords=stopwords.words(stopfile)

    negtest_feats=[(bag_of_words(negative_review),'neg') for negative_review in negative_reviews]
    postest_feats=[(bag_of_words(positive_review),'pos') for positive_review in positive_reviews]
    test_neg=len(negtest_feats)
    test_pos=len(postest_feats)
    testfeats=negtest_feats[:test_neg]+postest_feats[:test_pos]
    
    while(flag==1):                 #this flag is set so that user gets option to pass another query
        i = 0                       #i is set for indexing the 10 extracted videos
        result = []                 #double dimensional array to store 100 comments of each video
        pos_neg_list = []           #this list stores the positive and negative counts of all 10 videos as a tuple 
        query = raw_input('enter a query word:')
        (vid_ids, vid_titles,vid_likes,vid_dislikes,comment_count) = youtube_search(query) #youtube_search function returns five parameters
        print("no. of videos",len(vid_ids))
        
        nb_classifier=NaiveBayesClassifier.train(trainfeats)
        #nb_precisions, nb_recalls= precision_recall(nb_classifier, testfeats)

        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = nb_classifier.classify(feats)
            testsets[observed].add(i)
        
        
        print("Accuracy:",nltk.classify.accuracy(nb_classifier, testfeats))
        print("Positive Precision:",precision(refsets['pos'], testsets['pos']))
        print('Positive Recall:', recall(refsets['pos'], testsets['pos']))
        print('Positive F-measure:',f_measure(refsets['pos'], testsets['pos']))
        print("Negative Precision:",precision(refsets['neg'], testsets['neg']))
        print('Negative Recall:', recall(refsets['neg'], testsets['neg']))
        print('Negative F-measure:', f_measure(refsets['neg'], testsets['neg'])) 
        
        for vid_id in vid_ids:
            probs=[]                #this list stores the pos or neg tag for each comment of a video and is reinitialized to zero for next video
            
            print "\n"
            print i+1, ". VIDEO TITLE: ",vid_titles[i]
            print "no. of likes: ",vid_likes[i]
            print "no. of dislikes: ",vid_dislikes[i]
            print "no. of total comments: ",comment_count[i]
            comment = get_comment_threads(youtube,vid_id)   #getting comments list(100) 
            result.append(comment)
            print "no.of comments extracted", len(result[i])

            fig, ax=plt.subplots()
            rects1=ax.bar(ind, vid_likes[i],width, color='r')
            rects2=ax.bar(ind+width, vid_dislikes[i],width,color='y')
            ax.set_ylabel('Count')
            ax.set_title('Likes and Dislikes Chart')
            ax.set_xticklabels(('G1'))

            ax.legend((rects1[0], rects2[0]), ('Likes','Dislikes'))

            def autolabel(rects):
                for rect in rects:
                    height=rect.get_height()
                    ax.text(rect.get_x()+rect.get_width()/2., 1.05*height,
                            '%d' % int(height),
                            ha='center', va='bottom')
            autolabel(rects1)
            autolabel(rects2)

            #plt.show()
            #plot=plt.fig()
            figname="img"+str(i)+".png"
            plt.savefig(figname)

            for j in range(0,len(result[i])):
                result[i][j] = result[i][j].encode('ascii','ignore')
                splitted_data = result[i][j].split()        #splitting each comment of a video
                bag = bag_of_words1(set(splitted_data)-set(badwords))
                testfeats = bag
#                print j,'Classification:', nb_classifier.classify(testfeats)
                probs.append(nb_classifier.classify(testfeats))

            c=Counter(probs)
            print c            #printing the total pos and neg counts in 100 comments
            positive_count=c['pos']
            negative_count=c['neg']
            print "like and dislike ratio", (vid_likes[i]/vid_dislikes[i])
            print "pos neg ratio", (positive_count/ negative_count)
            pos_neg_list.append((positive_count,negative_count))

            fig, ax=plt.subplots()
            bars1=ax.bar(ind, pos_neg_list[i][0],width, color='r')
            bars2=ax.bar(ind+width, pos_neg_list[i][1],width,color='y')
            ax.set_ylabel('Count')
            ax.set_title('Positive and Negative Count')
            ax.set_xticklabels(('G1'))

            ax.legend((bars1[0], bars2[0]), ('Positive','Negative'))

            def autolabel(bars):
                for rect in bars:
                    height=rect.get_height()
                    ax.text(rect.get_x()+rect.get_width()/2., 1.05*height,
                            '%d' % int(height),
                            ha='center', va='bottom')
            autolabel(bars1)
            autolabel(bars2)

            #plt.show()
            #plot=plt.fig()
            figname="image"+str(i)+".png"
            plt.savefig(figname)
            i=i+1
        print pos_neg_list
            
        flag=int(raw_input("do you want to enter another query?(1 for yes and 0 for no: )"))
        
        
