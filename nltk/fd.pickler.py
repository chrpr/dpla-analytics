import time
import nltk
import pickle
import re
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.corpus import stopwords

colls = ["artstor","biodiv","rumsey","commonwealth","georgia","harvard",
        "ia","getty","kentucky","minnesota","missouri","mwdl","nara","nocar",
        "smiths","socar","texas","gpo","illinois","usc","virginia","nocoll"]

stats = pickle.load( open( "/media/storage/dpla-data/pickles/new/stats.p", "rb" ) )
lowercommon = {}

for coll in colls:
	filtered = pickle.load( open( "/media/storage/dpla-data/pickles/new/"+coll+"_filtered.p", "rb"))
	print(coll)
	fd = nltk.FreqDist(token.lower() for token in filtered)
	stats[coll]["lowerhaps"] = len(fd.hapaxes())
	pickle.dump( fd, open( "/media/storage/dpla-data/pickles/new/"+coll+"_fd.p", "wb"))
	print("Coungint Hapaxes and collecting most-common")
	print(stats[coll]["lowerhaps"])
	lowercommon[coll] = fd.most_common(200)
pickle.dump( stats, open( "/media/storage/dpla-data/pickles/new/newstats.p", "wb" ) )
pickle.dump( lowercommon, open( "/media/storage/dpla-data/pickles/new/lower_common.p", "wb" ) )
