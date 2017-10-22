#!/usr/bin/env python

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://mcss.mosra.cz'

OUTPUT_PATH = 'published/'
DELETE_OUTPUT_DIRECTORY = True

CSS_FILES = ['https://fonts.googleapis.com/css?family=Source+Code+Pro:400,400i,600%7CSource+Sans+Pro:400,400i,600&amp;subset=latin-ext',
             STATIC_URL.format(path='static/m-dark.compiled.css')]

PAGE_URL = 'http://mcss.mosra.cz/{slug}/'
ARTICLE_URL = 'http://mcss.mosra.cz/{category}/{slug}/'
