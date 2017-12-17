# -*- coding: utf-8 -*-
"""
Created on Fri Jul 07 16:40:28 2017

@author: alvarna
"""

import urllib
from urlparse import urljoin
import wget
from bs4 import BeautifulSoup
import logging

url = "http://sanskrit.uohyd.ac.in/Corpus/"
outdir = "sandhi_test_data"

content = urllib.urlopen(url).read()
doc = BeautifulSoup(content, 'html.parser')

logging.info("Fetching Sandhi-extracted files ...")
for link in doc.find_all('a'):
    if link.contents[0].endswith("Extracted") and link.get('href').endswith(".txt"):
        src = link.get('href')
        if not src.startswith('http'):
            src = urljoin(url, src)
        logging.info("Fetching " + src)
        wget.download(src, out=outdir)

logging.info("Finished")
