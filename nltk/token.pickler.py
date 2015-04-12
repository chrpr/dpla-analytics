import time
import nltk
import pickle
import re
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.corpus import stopwords

reader = CategorizedPlaintextCorpusReader('/media/storage/dpla-data/words/colls/', r'.*\.txt', cat_pattern=r'(\w+)\.txt')

# Removing oversized collections: hathi, nypl; Also, chunking them out:
# First batch represents what was completed on 4/10-4/11. 
#colls = ["artstor","biodiv","rumsey","commonwealth","georgia","harvard"]
#colls = ["ia","getty","kentucky","minnesota","missouri","mwdl"]
colls = ["nara","nocar","smiths","socar","texas","gpo","illinois","usc","virginia","nocoll"]

#data = {}

for coll in colls:
    print(reader.categories(coll+".txt"))
    data = {}
    data[coll] = {}
    data[coll]["stats"] = {}
    # 'kay. Can't pickle words. It's a stream reader.
    # But maybe you can if you tokenize we regex
    # Which also pulls out punctuation
    words = re.split(r'\W+', reader.raw(coll+'.txt'))
    data[coll]["words"] = words
    #words = reader.words(coll+".txt")
    #data[coll]["words"] = reader.words(coll+".txt")
    print("getting count " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    data[coll]["stats"]["wc"] = len(words)
    print(data[coll]["stats"]["wc"])
    print("getting uniq " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    data[coll]["stats"]["uniq"] = len(set([w.lower() for w in words]))
    print(data[coll]["stats"]["uniq"])
    print("filtering " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    data[coll]["filtered"] = [w for w in words if w.lower() not in nltk.corpus.stopwords.words('english')]
    print("getting filter count " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    data[coll]["stats"]["fwc"] = len(data[coll]["filtered"])
    print(data[coll]["stats"]["fwc"])
    print("getting filter uniq " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    data[coll]["stats"]["funiq"] = len(set([w.lower() for w in data[coll]["filtered"]]))
    print(data[coll]["stats"]["funiq"])
    #Maybe can't pickle frequency dists? If not, I'll have to fire 'em up later.
    #Or maybe pull their most common?
    #print("getting freqdist " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    #data[coll]["fd"] = nltk.FreqDist((token) for token in data[coll]["filtered"])
    pickle.dump( data, open( "/media/storage/dpla-data/pickles/"+coll+".p", "wb" ) )