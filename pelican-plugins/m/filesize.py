import os
import gzip
from docutils import nodes
from docutils.parsers import rst
from pelican import signals

settings = {}

def init(pelicanobj):
    settings['path'] = pelicanobj.settings.get('PATH', 'content')
    pass

def filesize(name, rawtext, text, lineno, inliner, options={}, content=[]):
    size = os.path.getsize(text.format(filename=os.path.join(os.getcwd(), settings['path'])))

    for unit in ['','k','M','G','T']:
        if abs(size) < 1024.0:
            size_string = "%3.1f %sB" % (size, unit)
            break
        size /= 1024.0
    else: size_string = "%.1f PB" % size

    return [nodes.inline(size_string, size_string)], []

def filesize_gz(name, rawtext, text, lineno, inliner, options={}, content=[]):
    with open(text.format(filename=os.path.join(os.getcwd(), settings['path'])), mode='rb') as f:
        size = len(gzip.compress(f.read()))

    for unit in ['','k','M','G','T']:
        if abs(size) < 1024.0:
            size_string = "%3.1f %sB" % (size, unit)
            break
        size /= 1024.0
    else: size_string = "%.1f PB" % size

    return [nodes.inline(size_string, size_string)], []

def register():
    signals.initialized.connect(init)

    rst.roles.register_local_role('filesize', filesize)
    rst.roles.register_local_role('filesize-gz', filesize_gz)
