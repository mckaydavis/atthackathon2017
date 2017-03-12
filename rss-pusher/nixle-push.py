#!/usr/bin/env python

# Creates a Device and a Stream associated with the device,
# then posts the current time every 10 seconds.
#
# Usage:
#   $ API_KEY=<YOUR APIKEY> python example.py

import os

RSS_FEEDS = """
https://agency.nixle.com/pubs/feeds/latest/13285
https://agency.nixle.com/pubs/feeds/latest/3182
https://agency.nixle.com/pubs/feeds/latest/3263
"""

M2X_KEY=os.environ['M2X_KEY']
DEVICE_ID = os.environ['DEVICE']


import time
import feedparser
from m2x.client import M2XClient
import urllib2
from lxml import etree


import sys
import pprint

pp = pprint.PrettyPrinter(indent=2)


def main(argv):
    # Instantiate a client
    client = M2XClient(key=M2X_KEY)

    # Create a device
    #device = client.create_device(
    #    name='Current Time Example',
    #    description='Store current time every 10 seconds',
    #    visibility='public'
    #)



    allfeeds = parse_all_rss_feeds()


    title_stream = get_stream(client, "titles")
    priority_stream = get_stream(client, "priority")

    for timestamp, priority, title, timessec in allfeeds:
        title_stream.add_value(title, timestamp)
        priority_stream.add_value(priority, timestamp)

    return 0



def parse_all_rss_feeds():
    allfeeds = []
    rss_urls = [txt for txt in RSS_FEEDS.split() if txt]
    for url in rss_urls:
        allfeeds += convert_rss_feed(url)

    return allfeeds


def parse_tree(txt):
    return etree.fromstring(txt, etree.HTMLParser())



def get_stream(client, stream_name, device_id=None):
    device = client.device(DEVICE_ID if device_id is None else device_id)

    # Create a data stream associated with target Device
    try:
        stream = device.stream(stream_name)
    except:
        stream = device.create_stream(stream_name, type="alphanumeric")

    return stream



def py3load_url(url):
    import urllib.request
    with urllib.request.urlopen(url) as response:
        return response.read().decode("iso-8859-1")
    return ""


def load_url(url):
    response = urllib2.urlopen(url)
    return response.read()


def get_priority_from_url(url):
    txt = load_url(url)
    tree = parse_tree(txt)
    elems = tree.xpath("//span[contains(@class, 'priority')]")
    return elems[0].text if elems else "N/A"


def get_title(entry):
    txt = entry.title_detail.value
    txt = txt.split()
    lines = [""]
    for word in txt:
        newl = lines[-1] + " " + word
        if len(newl) > 21:
            lines.append(word)
        else:
            lines[-1] = newl
    return "|".join(lines)





def toiso(timetup):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', timetup)

def add_entry(entry):
    title = entry.title_detail.value
    timetup = entry.published_parsed

    # timetup = time.gmtime(time.mktime(timetup) - 86400)

    timestr = toiso(timetup)
    link = entry.link
    priority = getPriority(link)

    stream.add_value(title, timestr)
    print title
    print timestr

    pp.pprint(entry)


def get_entry_priority(entry):
    title = entry.title_detail.value
    timetup = entry.published_parsed
    timestr = toiso(timetup)
    link = entry.link
    print "link={}".format(link)

def get_priority(entry):
    return get_priority_from_url(entry.link)

def get_timestamp(entry):
    return toiso(entry.published_parsed)



def convert_rss_feed(rss_url):
    rss_feed = feedparser.parse(rss_url)
    feed = []
    for entry in rss_feed.entries:
        feed.append([get_timestamp(entry),
                     get_priority(entry),
                     get_title(entry),
                     time.mktime(entry.published_parsed)])
        sys.stderr.write("{}\n".format(feed[-1]))

    feed.sort(key=lambda x: x[-1])
    return feed


if __name__ == "__main__":
    sys.exit(main(sys.argv))




# And now register the current time every 10 seconds (hit ctrl-c to kill)
#while True:
#    stream.add_value(int(time.time()))
#    time.sleep(10)
