import time
import nltk
import pickle
import re
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.corpus import stopwords
from nltk import bigrams

### Updated 20151020
colls = ["artstor","biodiv","rumsey","commonwealth","georgia","harvard",
        "ia","getty","kentucky","minnesota","missouri","mwdl","nara","nocar",
        "smiths","socar","texas","gpo","illinois","usc","virginia","nocoll",
        "hathi","nypl"]

#stats = pickle.load( open( "/media/storage/dpla-data/pickles/new/stats.p", "rb" ) )
stats = pickle.load( open( "/media/storage/dpla-data/words/colls.oct/pickles/stats.p", "rb"))
lowercommon = {}

for coll in colls:
	filtered = pickle.load( open( "/media/storage/dpla-data/words/colls.oct/pickles/"+coll+"_filtered.p", "rb"))
	print(coll)
	lower = [token.lower() for token in filtered]
	lfd = nltk.FreqDist(lower)
	print(lfd.most_common(10))
	top = lfd.most_common(1)
	stats[coll]["lowerhaps"] = len(lfd.hapaxes())
	pickle.dump( lfd, open( "/media/storage/dpla-data/words/colls.oct/pickles/"+coll+"_lfd.p", "wb"))
	print("Coungint Hapaxes and collecting most-common")
	print(stats[coll]["lowerhaps"])
	#lowercommon[coll] = fd.most_common(200)
	print("Bigram Frequencies")
	bgs = list(bigrams(lower))
	bfd = nltk.FreqDist(bgs)
	print(bfd.most_common(10))
	cfd = nltk.ConditionalFreqDist(bgs)
	print("CFD for top word: " + top[0][0])
	print(cfd[top[0][0]].most_common(10))
	pickle.dump( bfd, open( "/media/storage/dpla-data/words/colls.oct/pickles/"+coll+"_bfd.p", "wb"))
	pickle.dump( cfd, open( "/media/storage/dpla-data/words/colls.oct/pickles/"+coll+"_cfd.p", "wb"))

pickle.dump( stats, open( "/media/storage/dpla-data/words/colls.oct/pickles/newstats.p", "wb" ) )
#pickle.dump( lowercommon, open( "/media/storage/dpla-data/pickles/new/lower_common.p", "wb" ) )
