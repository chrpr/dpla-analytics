#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
import sys
import codecs

# import the Auth Helper class
import hello_analytics_api_v3_auth

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

from dateutil import rrule
from datetime import datetime, timedelta
import dateutil.parser

first = dateutil.parser.parse("2013-04-08")
last = datetime.now()

#first = dateutil.parser.parse("2015-06-22")
#last = dateutil.parser.parse("2015-06-28")

#analyt = codecs.open('/media/Windows7_OS/dpla/new/dpla.analytics.weekly.csv', 'w', encoding='utf-8')
#logger = codecs.open('/media/Windows7_OS/dpla/new/analytics.log', 'a', encoding='utf-8')
#analyt.write("item|hits\n")
analyt = codecs.open('/media/storage/dpla-data/words/colls.oct/analytics/dpla.analytics.weekly.csv', 'w', encoding='utf-8')
logger = codecs.open('/media/storage/dpla-data/words/colls.oct/analytics/analytics.log', 'a', encoding='utf-8')
analyt.write("item|hits\n")

logger.write("\n\n##########\n##### " + str(last) + "\n##########\n\n")

counts = {}

def main(argv):
  # Step 1. Get an analytics service object.
  service = hello_analytics_api_v3_auth.initialize_service()

  try:
    # Step 2. Get the user's first profile ID.
    profile_id = get_first_profile_id(service)
    if profile_id:

        for sdate in rrule.rrule(rrule.WEEKLY, dtstart=first, until=last):
            edate = sdate + timedelta(days=6)
            print "Range is %s through %s" % (sdate.strftime("%Y-%m-%d"), edate.strftime("%Y-%m-%d"))
            logger.write("Range is %s through %s" % (sdate.strftime("%Y-%m-%d"), edate.strftime("%Y-%m-%d")))
            start = 1
            while start < 200000:
                print "Start = %s" % start
                data = get_data(service, profile_id, sdate.strftime("%Y-%m-%d"), edate.strftime("%Y-%m-%d"), start)
                store_data(data)
                print_pagination_info(data)
                print 'Next Link      = %s' % data.get('nextLink')
                logger.write("Hit Count = %s\n" % data.get('totalResults'))
                print 'Contains Sampled Data = %s' % data.get('containsSampledData')
                logger.write("Contains Sampled Data = %s\n\n" % data.get('containsSampledData'))

                if data.get('nextLink'): start += 10000
                else: start = 200000
    
        print_data(counts)

  except TypeError, error:
    # Handle errors in constructing a query.
    print ('There was an error in constructing your query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

  except AccessTokenRefreshError:
    # Handle Auth errors. 
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')

def get_first_profile_id(service):
  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    # Get the first Google Analytics account
    firstAccountId = accounts.get('items')[0].get('id')

    # Get a list of all the Web Properties for the first account
    webproperties = service.management().webproperties().list(accountId=firstAccountId).execute()

    if webproperties.get('items'):
      # Get the first Web Property ID
      firstWebpropertyId = webproperties.get('items')[0].get('id')

      # Get a list of all Views (Profiles) for the first Web Property of the first Account
      profiles = service.management().profiles().list(
          accountId=firstAccountId,
          webPropertyId=firstWebpropertyId).execute()

      if profiles.get('items'):
        # return the first View (Profile) ID
        return profiles.get('items')[0].get('id')

  return None

def get_results(service, profile_id):
  # Use the Analytics Service Object to query the Core Reporting API
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2012-03-03',
      end_date='2012-03-03',
      metrics='ga:sessions').execute()

# Note from 20150405: Looks like the way to tweak this is going to be:
#metrics: ga:searcheUniques
#dimensions: ga:searchKeyword
#sort: -ga:searchUniques
#Curious if there's other interesting stuff to add here...

def get_data(service, profile_id, sdate, edate, start):
  # Use the Analytics Service Object to query the Core Reporting API
  return service.data().ga().get(
    ids='ga:' + profile_id,
    start_date=sdate,
    end_date=edate,
    #metrics='ga:hits',
    metrics='ga:pageviews',
    dimensions='ga:pagePath',
    #sort='-ga:hits',
    sort='-ga:pageviews',    
    filters='ga:pagepath=~^/item/',
    #filters='ga:pagepath=~^/item/c5cf1632a8a2c137c9b0e7b093024e0a',
    start_index=start,
    max_results='10000').execute()

# def get_data(service, profile_id, sdate, edate, start):
#   # Use the Analytics Service Object to query the Core Reporting API
#   return service.data().ga().get(
#     ids='ga:' + profile_id,
#     start_date=sdate,
#     end_date=edate,
#     metrics='ga:searcheUniques',
#     dimensions='ga:searchKeyword',
#     sort='-ga:searchUniques',
#     start_index=start,
#     max_results='10000').execute()

def print_results(results):
  # Print data nicely for the user.
  if results:
    print 'First View (Profile): %s' % results.get('profileInfo').get('profileName')
    print 'Total Sessions: %s' % results.get('rows')[0][0]

def store_data(data):
  # Print data nicely for the user.
  if data and type(data.get('rows')) == list:
    print 'Type: %s' % type(data)
    #pprint.pprint(data)
    print 'Data Length: %s' % len(data.get('rows'))
    print 'First Results: %s' % data.get('rows')[0]
    for row in data.get('rows'):
        if row[0] in counts: 
            counts[row[0]] += int(row[1])
        else:
            counts[row[0]] = int(row[1])
    #json +=  data.get('rows')

  else:
    print 'No results found'

def print_pagination_info(results):
  print 'Items per page = %s' % results.get('itemsPerPage')
  print 'Total Results  = %s' % results.get('totalResults')
  print 'Previous Link  = %s' % results.get('previousLink')
  print 'Next Link      = %s' % results.get('nextLink')

def print_data(counts):
    print 'Total Items = %s' % len(counts)
    for k, v in counts.iteritems():
        analyt.write(k + "|" + str(v) + "\n")

if __name__ == '__main__':
  main(sys.argv)