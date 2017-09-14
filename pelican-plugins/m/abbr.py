from . import parse_link
from docutils import nodes
from docutils.parsers import rst

def abbr(name, rawtext, text, lineno, inliner, options={}, content=[]):
    abbr, title = parse_link(text)
    if not title:
        return [nodes.abbreviation(abbr, abbr)], []
    return [nodes.abbreviation(abbr, abbr, title=title)], []

def register():
    rst.roles.register_local_role('abbr', abbr)
