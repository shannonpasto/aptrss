#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2024 Shannon Pasto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import subprocess
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from datetime import datetime, UTC
import uuid

# set a vew variables
url_origin = ""  # required. your full url
url_pathname = ""  # optional. url subdirectory, default is index.xml
file_path = ""  # optional. local file system, default is /var/www/html/index.html
feed_name = ""  # optional. name of the feed, default is Apt Upgradeable Packages

date_now = datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')

# check and set variables as needed
if not url_origin:
    raise Exception("Error: url_origin not set. Can not continue")
elif not url_origin.endswith('/'):
    url_origin = f"{url_origin}/"

if not url_pathname:
    url_pathname = "index.xml"

if not file_path:
    file_path = "/var/www/html/index.xml"

if not feed_name:
    feed_name = "Apt Upgradeable Packages"

# do apt and grab the output
subprocess.run(['apt', 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
result = subprocess.run(['apt', 'list', '--upgradable'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
output = result.stdout.decode('utf-8')
lines = output.strip().split('\n')[1:]  # Skip the header line
packages = [line.strip() for line in lines]

# build the xml
rss = ET.Element('rss', version='2.0', attrib={'xmlns:atom': 'http://www.w3.org/2005/Atom'})
channel = ET.SubElement(rss, 'channel')

atom_link = ET.Element('atom:link', {
    'href': f"{url_origin}{url_pathname}",
    'rel': 'self',
    'type': 'application/rss+xml'
})
channel.append(atom_link)

title = ET.SubElement(channel, 'title')
title.text = f"{feed_name}"

link = ET.SubElement(channel, 'link')
link.text = f"{url_origin}"

description = ET.SubElement(channel, 'description')
description.text = "List of upgradable packages from apt"

lastBuildDate = ET.SubElement(channel, 'lastBuildDate')
lastBuildDate.text = date_now

generator = ET.SubElement(channel, 'generator')
generator.text = "python3"

item = ET.SubElement(channel, 'item')
item_title = ET.SubElement(item, 'title')
item_title.text = f"List of Upgradable Packages - {date_now}"
item_link = ET.SubElement(item, 'link')
item_link.text = f"{url_origin}"

item_description = ET.SubElement(item, 'description')
package_details = "<br>".join(packages)
item_description.text = f"The following packages are upgradable:<br>{package_details}"

guid = ET.SubElement(item, "guid", isPermaLink="false")
guid.text = str(uuid.uuid4())

pub_date = ET.SubElement(item, 'pubDate')
pub_date.text = date_now

# pretty the feed
rss_feed = parseString(ET.tostring(rss, encoding='utf-8').decode('utf-8')).toprettyxml(indent='  ')

# write out the file
with open(file_path, 'w') as f:
    f.write(rss_feed)
