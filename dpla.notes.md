dpla work

 (head -10 dplaran ; tail  -2 dplaran) | jq '.[] |  { provider: .provider.name } '

 Some links:
 http://www.commandlinefu.com/commands/view/1385/cat-stdout-of-multiple-commands
 http://jeroenjanssens.com/2013/09/19/seven-command-line-tools-for-data-science.html
 http://stedolan.github.io/jq/manual/

 | jq '.[1].originalRecord | keys' -- fuck yeah, jq 'keys' is awesome!

These kinds of constructs work:
charper@charper-ThinkPad-T530:/media/Windows7_OS/dpla$ jq 'if .[].originalRecord.subject then 1 else 0 end' dpla100 | sort | uniq -c      51 0
     48 1


     jq '.[].originalRecord as $rec |  if $rec.subject  then  $rec.subject else 0 end' dpla100 | sort | uniq -c 

This keeps getting awesomer: 

charper@charper-ThinkPad-T530:/media/Windows7_OS/dpla$ jq '.[].sourceResource as $rec |  if $rec.subject  then $rec.subject | length else 0 end' dpla100 | sort | uniq -c | sort -rn

This blThis blah as $rec sertup rules....

Wow: 93 subjects...
charper@charper-ThinkPad-T530:/media/Windows7_OS/dpla$ jq '.[].sourceResource as $rec |  if $rec.subject | length > 92 then $rec else empty end' dplaran 
    * Also, use of "empty" here is rockin!

  77858 [
  77858 ]
  54270   "collection",
  12911   "contributor",
  50653   "creator",
  55840   "date",
  56406   "description",
  24416   "extent",
  40341   "format",
  58257   "@id",
  47923   "identifier",
  10508   "isPartOf",
  34464   "language",
  30235   "publisher",
  31932   "relation",
      1   "rights"
  67905   "rights",
  31751   "spatial",
  22292   "specType",
  44066   "stateLocatedIn",
  55693   "subject",
   9190   "temporal",
   2423   "title"
  75434   "title",
  75434   "type"

Cool. So find the keys. There's you're list, above. Reduces to:

collection, contributor, creator, date, description, extent, format, @id, identifier, 
isPartOf, language, publisher, relation, rights, spatial, specType, stateLocatedIn, 
subject, temporal, title, type

Okay, so the parser.py code is going to likely work. Must test more tomorrow, including overnight.

Also, can get huge chunks of data out of google analytics, but maybe only 5000 urls at a time?
https://www.google.com/analytics/web/?authuser=1#report/content-pages/a28197764w53856508p54747607/%3F_u.date00%3D20131001%26_u.date01%3D20141107%26explorer-table.plotKeys%3D%5B%5D%26explorer-table.rowCount%3D45000%26explorer-table.filter%3Ditem%26explorer-graphOptions.selected%3Danalytics.nthMonth/

Might need to do something with the API to really make this work...

Thumbnails are just stuffed into the identifier field. Not sure if there's an easy way to measure out "uniqueness" there, but can at least do presence or absence.

Full run of data started at 6pm on 11/9. Has completed 5.2 mill by 9:30pm.
Finished: at End: Sun, 09 Nov 2014 22:48:24 +0000

So, it takes almost 5 hours to process the entirety.

20141110:

I've got this turned on it's head. It's too relational with "Columns" set to the field, then counts below. I need "presence / Absence", Count, and "field" as columns.
Here's the issue: http://stackoverflow.com/questions/25434578/tableau-multiple-data-into-one-graph-with-double-dimension-on-the-x-axis

When adding the melt feature, it takes much longer:

Start: Tue, 11 Nov 2014 19:00:44 +0000
End: Wed, 12 Nov 2014 06:51:18 +0000

That's almost 12 hours!!

And produces a huge ass file:
-rw------- 1 charper charper 7.0G Nov 12 06:51 dpla.melt.csv
 162963361  162963361 7450298847 dpla.melt.csv

'kay -- This needs to be enriched further:

* TODO: Add source info (Hub or Institution?) to melted record -- allow breakdown of field by provider

Regression for DPLA is pretty well captured in the today's notes...

Maybe I can reformat this in R via melt, but prob better to just build secondary output file...
http://www.rdocumentation.org/packages/data.table/functions/melt.data.table


Google Analytics Work: 
https://developers.google.com/resources/api-libraries/documentation/analytics/v3/python/latest/analytics_v3.data.html

Okay, so I've authenticated a basic app. and it works. 

I also found and authenticated the "test query builder tool":
https://ga-dev-tools.appspot.com/explorer/?dimensions=ga%253AlandingPagePath&metrics=ga%253Aentrances%252Cga%253Abounces&sort=-ga%253Aentrances

I think the report I want is probably somjething like this:
https://ga-dev-tools.appspot.com/explorer/?dimensions=ga%253ApagePath&metrics=ga%253Ahits&filters=ga%253Apagepath%253D~item%252F&sort=-ga%253Ahits&start-date=2012-11-05&end-date=2014-11-19&max-results=50

Which matched a bunch of stuff, and returned the top 50:
Your query matched 178708 results but the API only returned the following 50 results:
I've downloaded that sample data.

Hmmm -- So if I push it back to 2010, I get: 
Your query matched 172596 results but the API only returned the following 50 results:

But if I push it to Dec 2012, I get more... WTF?
Your query matched 179365 results but the API only returned the following 50 results:

2013-01-01 to today gives:
Your query matched 179970 results but the API only returned the following 50 results:


What about 2014-01-01?
170339

And if I give it full year 2013?
163897

Huh. Oh, right. So, this is because it's a count of uniq addy's. But still, how does it go _up_ as it goes later?

Trying to match the actual DPLA IDs in the Google Anatytics data. Not easy:

741c85bde

Okay, there's a way to find 'em all:
python merger.py | awk '{ if (length($0) != 32) print $0 }'

741c85bde
672b 21ecab3dccf9c746b1ccdd54772a
f33df8c0cb0a0ebc3356376c35d55a8
86776
86776
9b52a3db26d3ebaaebceb7d4eaa02e86@KyDigitalLib
ade66a22a0e8b47d5012eb1064013d726q=princess
0cad78ef1949f7235ee94b189b5c5acc00&q=princess
133ef5dfb56003b692440a36518fae
b8e5b04cf
d4e76965e42c4e454c905c43849c66d
d4e76965e42c4e454c905c43849c66d
ia--lettertomydearfr00mkim4
0cad78ef1949f7235ee94b189b5c5acc00
133ef5dfb56003b692440a36518fae10=✓&page_size=100&q=Japanese+Internment
1898
24264
2b046d1da19614cf1fb9c87d44ccd155‎
2d9e42d1b…
308a168355c169d072ba12085655e6765D=image&page_size=100&q=robot
4912178
4912178
517bc409-c04d-48d8-a96d-2cf274becfe5
517bc409-c04d-48d8-a96d-2cf274becfe5
694e110634feadc124d6ff9628308101http:
73e7a954cfc3693ad4d131cc0788595319
8a64a296b29cfd6f3a757cb06e7dfc18http:
a6d0chttp:
ade66a22a0e8b47d5012eb1064013d726
ae35e143306235bfd12e2e3025abdf
bd8eebac84be59b68a29eebd7d3c0d73=100&q=robot
e4fea0f0223a546b7d0db02698216ab1http:
ec0afe4c077c0999ee88060ba039780
http:
http:
survivalinspace

Am now tweaking this code to ignore this subset of crap.

Worked!

Okay, also, gawk for windows is kinda hard to use:
C:\dpla\new>gawk -F: "BEGIN { FS = \""|\"" } { print $22 }" dpla.merged.csv | sort | uniq -c


##### 20150408

Getting into the NLTK stuff while my data parsing cranks away

This seems to work for creating my reader:

from nltk.corpus.reader import CategorizedPlaintextCorpusReader

reader = CategorizedPlaintextCorpusReader('/media/storage/dpla-data/new/words-6mill/colls/', r'.*\.txt', cat_pattern=r'(\w+)\.txt')


awesome!


In [7]: reader.categories('gpo.txt')
Out[7]: ['gpo']

In [8]: gpowordsf = reader.words('gpo.txt')

In [9]: len(gpowordsf
   ...: )
Out[9]: 36675069

In [10]: len(set([w.lower() for w in reader.words('gpo.txt)]))
  File "<ipython-input-10-298f8c7f96ff>", line 1
    len(set([w.lower() for w in reader.words('gpo.txt)]))
                                                        ^
SyntaxError: EOL while scanning string literal


In [11]: len(set([w.lower() for w in reader.words('gpo.txt')]))
Out[11]: 437150

Checkit!

In [13]: cfd = nltk.ConditionalFreqDist(
(genre, word)
for genre in ['gpo', 'artstor']
for word in reader.words(categories=genre))


In [14]: formats = ['image','text','moving','physical','object','Photographs']

In [15]: cfd.tabulate(samples=formats)
        image text moving physical object Photographs
artstor 56526  838   15 1066 1093 3655
    gpo 12370 153094  199 1770   22   73


So, when you're doing sort & uniq, and want to include the count in a delimited file, you can do this to grab the counts and put the pipes in:
sed -E "s/^\s*([0-9]*)\s*/\1|/"

* Always do a head > test.txt and test on that
* Then add -i to do it inline on the big guy

For example, this also helps me clean up my unicode shite:
sed -E -i "s/\{u'name': u//g; s/\}//g; s/\[//; s/\]//" subjects.txt 

20150411: Fuck. Memory issues abound in processing Hathitrust:

(py3k)charper@KARMS-325-PC02L:~/Dropbox/dpla/nltk$ python token.pickler.py
['artstor']
getting count Fri, 10 Apr 2015 23:48:36 +0000
8466030
getting uniq Fri, 10 Apr 2015 23:48:47 +0000
60760
filtering Fri, 10 Apr 2015 23:49:00 +0000
getting filter count Sat, 11 Apr 2015 00:03:27 +0000
6518566
getting filter uniq Sat, 11 Apr 2015 00:03:27 +0000
60635
['biodiv']
getting count Sat, 11 Apr 2015 00:03:31 +0000
8361216
getting uniq Sat, 11 Apr 2015 00:03:48 +0000
94755
filtering Sat, 11 Apr 2015 00:04:08 +0000
getting filter count Sat, 11 Apr 2015 00:18:33 +0000
7638579
getting filter uniq Sat, 11 Apr 2015 00:18:33 +0000
94631
['rumsey']
getting count Sat, 11 Apr 2015 00:18:38 +0000
15404401
getting uniq Sat, 11 Apr 2015 00:18:55 +0000
47763
filtering Sat, 11 Apr 2015 00:19:15 +0000
getting filter count Sat, 11 Apr 2015 00:45:26 +0000
12562369
getting filter uniq Sat, 11 Apr 2015 00:45:26 +0000
47643
['commonwealth']
getting count Sat, 11 Apr 2015 00:45:33 +0000
17539494
getting uniq Sat, 11 Apr 2015 00:46:05 +0000
205346
filtering Sat, 11 Apr 2015 00:46:38 +0000
getting filter count Sat, 11 Apr 2015 01:16:14 +0000
205220
['georgia']
getting count Sat, 11 Apr 2015 01:16:23 +0000
53640439
getting uniq Sat, 11 Apr 2015 01:17:41 +0000
151906
filtering Sat, 11 Apr 2015 01:19:06 +0000
getting filter count Sat, 11 Apr 2015 02:49:46 +0000
44265379
getting filter uniq Sat, 11 Apr 2015 02:49:46 +0000
151779
['harvard']
getting count Sat, 11 Apr 2015 02:50:15 +0000
1245233
getting uniq Sat, 11 Apr 2015 02:50:18 +0000
36383
filtering Sat, 11 Apr 2015 02:50:20 +0000
getting filter count Sat, 11 Apr 2015 02:52:28 +0000
1126322
getting filter uniq Sat, 11 Apr 2015 02:52:28 +0000
36265
['hathi']
getting count Sat, 11 Apr 2015 02:52:29 +0000
221877275
getting uniq Sat, 11 Apr 2015 02:59:28 +0000
8544108
filtering Sat, 11 Apr 2015 03:10:31 +0000
getting filter count Sat, 11 Apr 2015 09:31:06 +0000
200886718
getting filter uniq Sat, 11 Apr 2015 09:31:06 +0000
Killed

I should probably kick this off again, but leaving Hathi & NYPL out of the picture...

Actually doing it in chunks, and changing up routine.

Was making words out of reader stream.  -- words = reader.words(coll+".txt"):
['ia']
getting count Sat, 11 Apr 2015 10:24:12 +0000
29337722
getting uniq Sat, 11 Apr 2015 10:24:57 +0000
504635
filtering Sat, 11 Apr 2015 10:25:48 +0000

But this included punctuation.
Now making words out vi regex tokenization. --  words = re.split(r'\W+', reader.raw(coll+'.txt'))

Maybe this will also allow me to pickle the words? Might be slower, though.
(py3k)charper@KARMS-325-PC02L:~/Dropbox/dpla/nltk$ python token.pickler.py
['ia']
getting count Sat, 11 Apr 2015 10:50:00 +0000
29337722
getting uniq Sat, 11 Apr 2015 10:50:44 +0000
504635
filtering Sat, 11 Apr 2015 10:51:35 +0000

Top Facets:

1 2 3 4 5
United States399760
Places385140
Texas380381
Business, Economics and Finance311406
Communications284120
Newspapers283024
Advertising278941
Death--Proof and certification--Utah277397
Journalism272220
Anthropology269371
Photographs243081
Plantae242475
Dicotyledonae187019
Animalia179219
New York Worlds Fair (1939-1940)s Fair (1939-1940)175861
Archaeology147202
Dwellings147012
Housing areas134181
Ethnology125298
Type Register103087
Arthropoda102062
Cigarette cards98182
Landscape and Nature90291
Stereoscopic views84544
Geography and Maps83110
Portraits82894
People69425
Insects68778
Menus65703
Social Life and Customs64558
Go to top navigation
Go to main navigation
Go to search form
Go to main content
Go to social media navigation
DPLA: Digital Public Library of America
About 
Staff
Board & Committees
Funding
History
Policies
Projects
Awards
Hubs 
Become a Hub
For Developers 
API Codex
Ideas & Projects
Bulk Download
Sample Code & Libraries
Metadata Application Profile
Get Involved 
Community Reps
Open Calls
Events
DPLAfest 2015
Follow Us
Shop
Help 
Tutorials
FAQ
DPLA Accounts
News 
Press
Contact 
Jobs
Donate
Login
Sign Up
Home
Exhibitions
Map
Timeline
Bookshelf
Apps
View:
List
Map
Timeline
Bookshelf Search the Library  SaveShare



Search Results
Your search for * returned 9,060,858 results.
Items per page: Sort by: 
1 2 3 ... 906085 906086
207-dp-9093a-si3428_t
IMAGE

Swearing-in Ceremony for Assistant Secretary Keith Nelson - Secretary Alphonso Jackson swearing in Keith Nelson as Assistant Secretary for Administration, at HUD Headquarters
Department of Housing and Urban Development. Office of Administrative and Management Services. Multimedia Division. Publications Branch. Multimedia Library, (2000 -)

View Object 
207-dp-9097-dsc_0046_t
IMAGE

60th Birthday Event for Secretary Alphonso Jackson - Celebration marking Secretary Alphonso Jackson's 60th birthday
Department of Housing and Urban Development. Office of Administrative and Management Services. Multimedia Division. Publications Branch. Multimedia Library, (2000 -)

View Object 
207-dp-9073-pa3067_t
IMAGE

Secretary Alphonso Jackson with HUD Regional Public Affairs Officers - Secretary Alphonso Jackson meeting with HUD Regional Public Affairs Officers at HUD Headquarters
Department of Housing and Urban Development. Office of Administrative and Management Services. Multimedia Division. Publications Branch. Multimedia Library, (2000 -)

View Object 
95-gp-5192-box0882_026_001_ac_t
IMAGE

Road Construction - Oregon
Department of Agriculture. Forest Service.  (07/01/1905 -)

View Object 
207-dp-9068-dsc_3372_t
IMAGE

Secretary Alphonso Jackson at Historically Black Colleges and Universities Awards Ceremony - Secretary Alphonso Jackson presenting Historically Black Colleges and Universities (HBCU) Awards, Hyatt Regency Hotel, Washington, D.C
Department of Housing and Urban Development. Office of Administrative and Management Services. Multimedia Division. Publications Branch. Multimedia Library, (2000 -)

View Object 
207-dp-9093c-si3433_t
IMAGE

Swearing-in Ceremony for Assistant Secretary Kim Kendrick - Secretary Alphonso Jackson swearing in Kim Kendrick as Assistant Secretary for Fair Housing and Equal Opportunity, at HUD Headquarters
Department of Housing and Urban Development. Office of Administrative and Management Services. Multimedia Division. Publications Branch. Multimedia Library, (2000 -)

View Object 
95-gp-5190-box0881_061_001_ac_t
IMAGE

Road Construction - North Carolina
Department of Agriculture. Forest Service.  (07/01/1905 -)

View Object 
207-dp-9093-dsc_3452_t
IMAGE

Swearing-in Ceremony for Assistant Secretaries - Secretary Alphonso Jackson, staff at swearing-in proceedings for Keith Nelson (Assistant Secretary for Administration), Darlene Williams (Assistant Secretary for Policy Development and Research), Kim Kendrick (Assistant Secretary for Fair Housing and Equal Opportunity), and Keith Gottfried (General Counsel), HUD Headquarters
Department of Housing and Urban Development. Office of Administrative and Management Services. Multimedia Division. Publications Branch. Multimedia Library, (2000 -)

View Object 
95-gp-5200-box0883_028_001_ac_t
IMAGE

Road Construction - Virginia
Department of Agriculture. Forest Service.  (07/01/1905 -)

View Object 
95-gp-5259-box0891_040_001_ac_t
IMAGE

Signs - Colorado
Department of Agriculture. Forest Service.  (07/01/1905 -)

View Object 
Refine

By Format
text4470900
image4283155
moving image22731
physical object11924
sound9894
More »
Contributing Institution
National Archives at College Park - Still Pictures439935
Harvard University405345
University of California379541
University of Michigan372224
Utah State Archives300218
More »
Partner
HathiTrust2340825
The New York Public Library1239848
Smithsonian Institution1046327
Mountain West Digital Library919023
National Archives and Records Administration700948
More »
By Date
From

United States399760
Places385140
Texas380381
Business, Economics and Finance311406
Communications284120
Insecta64243
Native Americans62521
Government and Law60220
Periodicals59915
Education56833
Maps54624
Architecture51016
Dead50439
American newspapers--Sections, columns, etc.--Genealogy50198
Obituaries--Georgia--Gordon County50197
Death notices--Georgia--Gordon County50197
Hymenoptera49103
Men48276
Exhibitions44680
Bureau Of American Ethnology44388
Apidae44253
Monocotyledonae43993
Coins, Currency and Medals42316
Buildings42079
Bureau of Engraving and Printing41772
Women40553
Georgia--Social life and customs--20th century39647
Statistical areas39572
Census--Maps39571
Census blocks39265
U.S. Department of the Treasury38594
United States--History--Civil War, 1861-186535692
Utah35064
Agriculture34966
Crowdsourcing Project34307
Correspondence33821
(1900-1929) North Carolina's industrial revolution and World War One33388
Sheet music33382
Prehistoric32683
Students31999
United States--History--Civil War, 1861-1865--Veterans30305
Military pensions--North Carolina30211
Children30138
New York World's Fair (1939-1940)29845
Natural resources29476
Schools29146
Transportation27533
Colleges and Universities27512
Chordata27320
Cyperales26938
Annelida26097
Group portraits25853
Underwood & Underwood24750
Survey maps24488
Government24488
Topographic maps24473
Topography24166
Quadrangle maps23987
Historical Collections23827
GPI23827
Texas--Maps, Topographic23685
Elevations23673
Geologic surveys23557
Texas--Surveys23548
Geologic maps23544
Horses23469
Trees23377
Poaceae23372
African Americans22575
Elected Officials22245
Birds22051
Rosales21839
Individuals21760
Automobiles21486
Euphorbiaceae21484
Euphorbiales21399
Archival materials21054
Malacostraca20558
Flowers20370
Fishes20211
(1990-current) Contemporary20124
Prints20067
Savannah (Ga.)--Newspapers19966
Chatham County (Ga.)--Newspapers19960
Laws--Texas19949
Requests19906
Attorney Generals19874
Attorneys general's opinions--Texas19866
Written statements19865
Legal questions19865
Legal interpretations19865
Asteraceae19824
Asterales19819
Ads19526
Polychaeta19398
Japan19376
Polychaetes19319
World War, 1939-194519203
Indians of North America19048
Art18913
Diaries18629
Landscapes18626
Government and politics18251
Harris County17721
History17591
Natural history17498
Dallas County17469
Environmental protection17453
Catalogs17400
Military and War17346
Houses17313
Taylor County17253
Rivers17217
Widows17009
El Paso County16948
Botany16944
Parks16943
Clubs and Organizations16909
Arts and Crafts16734
Abilene16619
Pollution16215
China16114
Mountains13042
Ski Archives12754
Landscape9602

FYI -- Bad files on the work box are: georgia & dpla itself (under new and under 6-mill).
THis affects dev/sda7 on the ATA WDC WDIVEALX-759BA1 drive
  * I've already contated Beatrice about this issue.
  * Whooo!