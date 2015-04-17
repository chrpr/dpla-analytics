import pickle
import nltk

colls = ["artstor","biodiv","rumsey","commonwealth","georgia","harvard",
        "ia","getty","kentucky","minnesota","missouri","mwdl",
        "nara","nocar","smiths","socar","texas","gpo","illinois","usc","virginia","nocoll"]

fd = pickle.load( open( "/media/storage/dpla-data/pickles/new"+coll+"_fd.p", "rb" ) )

for c in colls:
    fd = pickle.load( open( "/media/storage/dpla-data/pickles/new"+coll+"_fd.p", "rb" ) )
    print("\nBuilding FD for " + c)
    fd = nltk.FreqDist((token) for token in c)
