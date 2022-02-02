from __future__ import absolute_import
import sys

if sys.version_info.major == 2:
    from pyximport._pyximport2 import install, uninstall, show_docs
else:
    from pyximport._pyximport3 import install, uninstall, show_docs

if __name__ == '__main__':
    show_docs()
