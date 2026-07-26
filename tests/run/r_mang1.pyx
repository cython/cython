# mode: run

__doc__ = u"""
    >>> import re
    >>> t
    ('2',)
    >>> t == re.search(r'(\\d+)', '-2.80 98\\n').groups()
    True
"""

# this is a string constant test, not a test for 're'

import re
t = re.search(u'(\d+)', u'-2.80 98\n').groups()
