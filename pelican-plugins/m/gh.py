#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#

from . import parse_link
from docutils import nodes
from docutils.parsers import rst

def gh_internal(account, ref, title, link):
    base_url = "https://github.com/{}/{}/{}/{}"
    if '#' in ref:
        project, _, issue = ref.partition('#')
        url = base_url.format(account, project, "issues", issue)
        if not title: title = link
    elif '@' in ref:
        project, _, commit = ref.partition('@')
        url = base_url.format(account, project, "commit", commit)
        if not title: title = account + "/" + project + "@" + commit[0:7]
    elif '$' in ref:
        project, _, branch = ref.partition('$')
        url = base_url.format(account, project, "tree", branch)
        if not title: title = url
    elif '^' in ref:
        project, _, branch = ref.partition('^')
        url = base_url.format(account, project, "releases/tag", branch)
        if not title: title = url
    else:
        url = "https://github.com/{}/{}".format(account, ref)
        if not title:
            # if simple profile link, no need to expand to full URL
            title = link if not '/' in ref else url

    return title, url

def gh(name, rawtext, text, lineno, inliner, options={}, content=[]):
    title, link = parse_link(text)
    account, _, ref = link.partition('/')
    if not ref:
        url = "https://github.com/{}".format(account)
        if not title: title = "@{}".format(account)
    else:
        title, url = gh_internal(account, ref, title, link)

    node = nodes.reference(rawtext, title, refuri=url, **options)
    return [node], []

def register():
    rst.roles.register_local_role('gh', gh)
