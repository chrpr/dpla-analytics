import pickle
import nltk

colls = ["artstor","biodiv","rumsey","commonwealth","georgia","harvard",
        "ia","getty","kentucky","minnesota","missouri","mwdl",
        "nara","nocar","smiths","socar","texas","gpo","illinois","usc","virginia","nocoll"]


for c in colls:
    p = pickle.load( open( "/media/storage/dpla-data/pickles/"+c+".p", "rb" ) )
    print("\nGathering Stats for " + c)