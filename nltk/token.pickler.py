import time
import nltk
import pickle
import re
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.corpus import stopwords

reader = CategorizedPlaintextCorpusReader('/media/storage/dpla-data/words/colls/', r'.*\.txt', cat_pattern=r'(\w+)\.txt')

# Removing oversized collections: hathi, nypl; Also, chunking them out:
# First batch represents what was completed on 4/10-4/11. 
colls = ["searches"]
#colls = ["artstor","biodiv","rumsey","commonwealth","georgia","harvard",
#        "ia","getty","kentucky","minnesota","missouri","mwdl","nara","nocar",
#        "smiths","socar","texas","gpo","illinois","usc","virginia","nocoll"]
#colls = ["ia","getty","kentucky","minnesota","missouri","mwdl"]
#colls = ["nara","nocar","smiths","socar","texas","gpo","illinois","usc","virginia","nocoll"]

#data = {}
stats = {}
common = {}

for coll in colls:
    print(reader.categories(coll+".txt"))
    stats[coll] = {}
    # 'kay. Can't pickle words. It's a stream reader.
    # But maybe you can if you tokenize we regex
    # Which also pulls out punctuation
    print("prep & pickle words")
    words = re.split(r'\W+', reader.raw(coll+'.txt'))
    pickle.dump( words, open( "/media/storage/dpla-data/pickles/new/"+coll+"_words.p", "wb"))
    #words = reader.words(coll+".txt")
    #data[coll]["words"] = reader.words(coll+".txt")
    print("getting count " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    stats[coll]["wc"] = len(words)
    print(stats[coll]["wc"])
    print("getting uniq " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    stats[coll]["uniq"] = len(set([w.lower() for w in words]))
    print(stats[coll]["uniq"])
    print("filtering & pickling " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    filtered = [w for w in words if w.lower() not in nltk.corpus.stopwords.words('english')]
    pickle.dump( filtered, open( "/media/storage/dpla-data/pickles/new/"+coll+"_filtered.p", "wb"))
    print("getting filter count " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    stats[coll]["fwc"] = len(filtered)
    print(stats[coll]["fwc"])
    print("getting filter uniq " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    stats[coll]["funiq"] = len(set([w.lower() for w in filtered]))
    print(stats[coll]["funiq"])
    print("getting and pickling frequency distributions")
    fd = nltk.FreqDist((token) for token in filtered)
    stats[coll]["haps"] = len(fd.hapaxes())
    pickle.dump( fd, open( "/media/storage/dpla-data/pickles/new/"+coll+"_fd.p", "wb"))
    print("Coungint Hapaxes and collecting most-common")
    print(stats[coll]["haps"])
    common[coll] = fd.most_common(200)
    #common.extend(fd.most_common(100))
    print("common is now: ", len(common))
    #Maybe can't pickle frequency dists? If not, I'll have to fire 'em up later.
    #Or maybe pull their most common?
    #print("getting freqdist " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    #data[coll]["fd"] = nltk.FreqDist((token) for token in data[coll]["filtered"])


pickle.dump( stats, open( "/media/storage/dpla-data/pickles/new/sear_stats.p", "wb" ) )
pickle.dump( common, open( "/media/storage/dpla-data/pickles/new/sear_common.p", "wb" ) )