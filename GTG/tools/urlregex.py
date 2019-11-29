"""
Detects urls using regex

Based on
https://dev.twitter.com/docs/tco-url-wrapper/how-twitter-wrap-urls
"""

import re

UTF_CHARS = r'a-z0-9_\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff'

SUBST_DICT = {
    "pre": r'(?:[^/"\':!=]|^|\:)',
    "domain": r'([\.-]|[^\s_\!\.\/])+\.[a-z]{2,}(?::[0-9]+)?',
    "path": r'(?:[\.,]?[%s!\*\'\(\);:&=\+\$/%s#\[\]\-_,~@])' % (
        UTF_CHARS, '%'),
    "query": r'[a-z0-9!\*\'\(\);:&=\+\$/%#\[\]\-_\.,~]',
    # Valid end-of-path characters (so /foo. does not gobble the period).
    "path_end": r'[%s\)=#/]' % UTF_CHARS,
    "query_end": '[a-z0-9_&=#]',
}

HTTP_URI = '((%(pre)s)((https?://|www\\.)(%(domain)s)(\/%(path)s*' \
    '%(path_end)s?)?(\?%(query)s*%(query_end)s)?))' % SUBST_DICT
FILE_URI = '(file:///(%(path)s*%(path_end)s?)?)' % SUBST_DICT

URL_REGEX = re.compile('%s|%s' % (HTTP_URI, FILE_URI), re.IGNORECASE)


def match(text):
    return re.match(URL_REGEX, text)
