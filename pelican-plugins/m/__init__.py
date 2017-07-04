#!/usr/bin/env python

from docutils import utils
import re

link_regexp = re.compile(r'(?P<title>.*) <(?P<link>.+)>')

def parse_link(text):
    link = utils.unescape(text)
    m = link_regexp.match(link)
    if m: return m.group('title', 'link')
    return None, link
