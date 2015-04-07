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


