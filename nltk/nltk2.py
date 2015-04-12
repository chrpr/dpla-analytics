import ijson
import codecs
import operator
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import glob
from datetime import datetime
from dateutil import tz
import nltk


show = "#Scandal"
jsons = glob.glob('../twarc/' + show + '*')
print show
print "WTF" + str(jsons)

