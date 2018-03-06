# -*- coding: utf-8 -*-
'''
OpenConfig package init
'''
from __future__ import absolute_import
from __future__ import unicode_literals

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution('openconfig').version
except pkg_resources.DistributionNotFound:
    __version__ = "Not installed"


__all__ = ('__version__')
