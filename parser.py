import ijson
import time
import codecs
from datetime import datetime
from time import strftime, localtime

f = open("/media/Windows7_OS/dpla/new/dpla")
out = codecs.open('/media/Windows7_OS/dpla/new/dpla.csv', 'w', encoding='utf-8')
melt = codecs.open('/media/Windows7_OS/dpla/new/dpla.melt.csv', 'w', encoding='utf-8')

now = ""
start =  time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
print "Start: " + start
counter = 0

melt.write("identifier|provider|subprov|field|binary|count\n")

header = "identifier|collection|contributor|creator|date|description|extent|format|identifier|"
header += "isPartOf|language|publisher|relation|rights|spatial|specType|stateLocatedIn|"
header += "subject|temporal|title|type|provider|subprov|thumbnail"
out.write(header + "\n")
for item in ijson.items(f, "item"):
    counter = counter + 1
    if counter % 10000 == 0:
        now = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
        print str(counter) + ": " + now
    ident = item['id']
    if "provider" in item: prov = item['provider']['name']
    else: prov = "Null"
    if "dataProvider" in item:
        if isinstance(item['dataProvider'], basestring): subprov = item['dataProvider']
        else: subprov = ", ".join(item['dataProvider'])
    else: subprov = "Null"
    string = ident
    # collection, contributor, creator, date, description, extent, format, @id, identifier, 
    # isPartOf, language, publisher, relation, rights, spatial, specType, stateLocatedIn, 
    # subject, temporal, title, type

    for field in ["collection", "contributor", "creator", "date", "description", 
                  "extent", "format", "identifier", "isPartOf", "language", "publisher", 
                  "relation", "rights", "spatial", "specType", "stateLocatedIn", 
                  "subject", "temporal", "title", "type"]: 

        if field in item['sourceResource'] and item['sourceResource'][field] is not None:
            melt.write(ident + "|" + prov + "|" + subprov + "|" + field + "|1") 
            if isinstance(item['sourceResource'][field], list):
                string += "|" + str(len(item['sourceResource'][field]))
                melt.write("|" + str(len(item['sourceResource'][field])) + "\n")
            else:  
                string += "|" + "1"
                melt.write("|1\n")
        else: 
            string += "|" + "0"
            melt.write(ident + "|" + prov + "|" + subprov +"|" + field + "|0|0\n")
    
    string += "|" + prov + "|" + subprov 
    if 'object' in item:
        string += "|" + "1"
        melt.write(ident + "|" + prov + "|" + subprov + "|thumb|1|1\n")
    else: 
        string += "|" + "0"
        melt.write(ident + "|" + prov + "|" + subprov + "|thumb|0|0\n")

    out.write(string + "\n")
#objects = ijson.items(f, 'sourceResource')
#for o in objects:
#    print 'title'

end = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())

print "Start: " + start
print "End: " + end