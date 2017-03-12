#!/usr/bin/env python

# Creates a Device and a Stream associated with the device,
# then posts the current time every 10 seconds.
#
# Usage:
#   $ API_KEY=<YOUR APIKEY> python example.py

import os
import time
import feedparser
from m2x.client import M2XClient

import pprint

pp = pprint.PrettyPrinter(indent=2)

# Instantiate a client
client = M2XClient(key=os.environ['M2X_KEY'])

# Create a device
#device = client.create_device(
#    name='Current Time Example',
#    description='Store current time every 10 seconds',
#    visibility='public'
#)

DEVICE_ID = os.environ['DEVICE']

device = client.device(DEVICE_ID)

# Create a data stream associated with target Device
try:
    stream = device.stream('titles')
except:
    stream = device.create_stream('titles', type="alphanumeric")


rss_feeds = """
https://agency.nixle.com/pubs/feeds/latest/3182
https://agency.nixle.com/pubs/feeds/latest/3263
"""

rss_feeds = [txt for txt in rss_feeds.split() if txt]

rssfeed = feedparser.parse(rss_feeds[0])

#pp.pprint(rssfeed)


def toiso(timetup):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', timetup)

for entry in rssfeed.entries:
    title = entry.title_detail.value
    timetup = entry.published_parsed

    # timetup = time.gmtime(time.mktime(timetup) - 86400)

    timestr = toiso(timetup)


    stream.add_value(title, timestr)
    print title
    print timestr
    pp.pprint(entry)




# And now register the current time every 10 seconds (hit ctrl-c to kill)
#while True:
#    stream.add_value(int(time.time()))
#    time.sleep(10)
