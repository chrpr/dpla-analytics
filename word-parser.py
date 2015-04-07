import ijson
import time
import codecs
from datetime import datetime
from time import strftime, localtime

f = codecs.open("/media/storage/dpla-data/new/dpla", 'r', encoding='utf-8')
# Main output file

#This bit of data structure won't work in standard IO.
#To do this right, I'll need a database (or mongo)
#out = codecs.open('/media/storage/dpla-data/new/words/words.json', 'w', encoding='utf-8')

fields = ["identifier","collection","contributor","creator","date","description",
          "extent","format","identifier","isPartOf","language","publisher",
          "relation","rights","spatial","specType","stateLocatedIn","subject",
          "temporal","title","type","provider","subprov","thumbnail"]

colls = {    "ARTstor": "artstor",
             "Biodiversity Heritage Library": "biodiv",
             "David Rumsey": "rumsey",
             "Digital Commonwealth": "commonwealth",
             "Digital Library of Georgia": "georgia",
             "Harvard Library": "harvard",
             "HathiTrust": "hathi",
             "Internet Archive": "ia",
             "J. Paul Getty Trust": "getty",
             "Kentucky Digital Library": "kentucky",
             "Minnesota Digital Library": "minnesota",
             "Missouri Hub": "missouri",
             "Mountain West Digital Library": "mwdl",
             "National Archives and Records Administration": "nara",
             "North Carolina Digital Heritage Center": "nocar",
             "Smithsonian Institution": "smiths",
             "South Carolina Digital Library": "socar",
             "The New York Public Library": "nypl",
             "The Portal to Texas History": "texas",
             "United States Government Printing Office (GPO)": "gpo",
             "University of Illinois at Urbana-Champaign": "illinois",
             "University of Southern California. Libraries": "usc",
             "University of Virginia Library": "virginia"     
        }

fieldfiles = {}
collfiles = {}

#fieldfiles[s] = [codecs.open('/media/storage/dpla-data/new/words/fields/%s.txt' %s, 'w', encoding='utf-8') for s in fields]
#collfiles[s] = [codecs.open('/media/storage/dpla-data/new/words/colls/%s.txt' %s, 'w', encoding='utf-8') for s in colls.itervalues()]


# for field in fieldfiles: print field

for s in fields:
   fieldfiles[s] = codecs.open('/media/storage/dpla-data/new/words/fields/%s.txt' %s, 'w', encoding='utf-8')
for s in colls.itervalues():
   collfiles[s] = codecs.open('/media/storage/dpla-data/new/words/colls/%s.txt' %s, 'w', encoding='utf-8')

# for k,v in fieldfiles.iteritems():
#     print k
#     print v

# collfiles = [codecs.open('/media/storage/dpla-data/new/words/colls/%s.txt' %s, 'w', encoding='utf-8') for s in colls.itervalues()]


nocoll = codecs.open('/media/storage/dpla-data/new/words/colls/none.txt', 'w', encoding='utf-8')

#write


now = ""
start =  time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
print "Start: " + start
counter = 0


for item in ijson.items(f, "item"):
    counter = counter + 1
    if counter % 10000 == 0:
        now = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
        print str(counter) + ": " + now
    if "provider" in item: 
        prov = item['provider']['name']
        cname = colls[prov]
        #print cname
    else: 
        prov = "Null"
        cname = "nocoll"
    if "dataProvider" in item:
        if isinstance(item['dataProvider'], basestring): subprov = item['dataProvider']
        else: subprov = ", ".join(item['dataProvider'])
    else: subprov = "Null"
    string = ""
    # collection, contributor, creator, date, description, extent, format, @id, identifier, 
    # isPartOf, language, publisher, relation, rights, spatial, specType, stateLocatedIn, 
    # subject, temporal, title, type

    for field in ["collection", "contributor", "creator", "date", "description", 
                  "extent", "format", "identifier", "isPartOf", "language", "publisher", 
                  "relation", "rights", "spatial", "specType", "stateLocatedIn", 
                  "subject", "temporal", "title", "type"]: 

        if field in item['sourceResource'] and item['sourceResource'][field] is not None:
            if isinstance(item['sourceResource'][field], list):
                for entry in item['sourceResource'][field]:
                    if isinstance(entry, dict):
                        # print field
                        # print entry
                        if 'title' in entry.keys():
                            string += unicode(entry['title']) + " "
                            fieldfiles[field].write(unicode(entry['title']) + " ")
                        elif 'displayDate' in entry.keys():
                            string += unicode(entry['displayDate']) + " "
                            fieldfiles[field].write(unicode(entry['displayDate']) + " ")
                        elif 'name' in entry.keys():
                            string += unicode(entry['name']) + " "
                            fieldfiles[field].write(unicode(entry['name']) + " ")
                        else:
                            string += unicode(entry) + " "
                            fieldfiles[field].write(unicode(entry) + " ")
                    elif entry is not None:
                        string += unicode(entry) + " "
                        fieldfiles[field].write(unicode(entry) + " ")
            elif isinstance(item['sourceResource'][field], dict):
                #print item['sourceResource'][field]
                if 'title' in item['sourceResource'][field].keys():
                    string += unicode(item['sourceResource'][field]['title']) + " "
                    fieldfiles[field].write(unicode(item['sourceResource'][field]['title']) + " ")
                elif 'displayDate' in item['sourceResource'][field].keys():
                    string += unicode(item['sourceResource'][field]['displayDate']) + " "
                    fieldfiles[field].write(unicode(item['sourceResource'][field]['displayDate']) + " ")
                else:
                    string += unicode(item['sourceResource'][field]['name']) + " "
                    fieldfiles[field].write(unicode(item['sourceResource'][field]['name']) + " ")
                #fieldfiles[f].write(item['sourceResource'][f]['title']) 
            else:  
                #print item['sourceResource'][field]
                string += unicode(item['sourceResource'][field]) + " "
                fieldfiles[field].write(unicode(item['sourceResource'][field]) + " ")
    
    string += " " + prov + " " + subprov + " "
    #print string
    #collfiles[cname].write(string + "\n")
    collfiles[cname].write(string + " ")

#objects = ijson.items(f, 'sourceResource')
#for o in objects:
#    print 'title'

end = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())

print "Start: " + start
print "End: " + end

# for f in fieldfiles:
#     close()
# for f in collfiles:
#     close()