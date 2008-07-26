__doc__ = u"""
    >>> import re
    >>> t
    (u'2',)
    >>> t == re.search('(\\d+)', '-2.80 98\\n').groups()
    True
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"(u'", u"('")

# this is a string constant test, not a test for 're'

import re
t = re.search(u'(\d+)', u'-2.80 98\n').groups()
