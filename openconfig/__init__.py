# -*- coding: utf-8 -*-
'''
OpenConfig package init
'''
from __future__ import absolute_import
from __future__ import unicode_literals

# Import Python stdlib
import os
import sys
import inspect
import logging
import importlib

# Import third party libraries
import napalm

import pkg_resources

log = logging.getLogger(__name__)

try:
    __version__ = pkg_resources.get_distribution('openconfig').version
except pkg_resources.DistributionNotFound:
    __version__ = "Not installed"


def get_network_driver(driver_name, lib=None):
    '''
    The network driver provider for python-openconfig.
    '''
    if lib:
        log.debug('Trying to use %s as the base library', lib)
        lib_mod = importlib.import_module(lib)
    else:
        log.debug('No library specified, relying on NAPALM')
        lib_mod = napalm
    napalm_driver = lib_mod.get_network_driver(driver_name)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    subdirs = [os.path.basename(d[0]) for d in os.walk(current_dir)]
    if driver_name not in subdirs[1:]:
        log.warning('%s is not an python-openconfig supported driver')
        return napalm_driver
    driver_import = 'openconfig.{}'.format(driver_name)
    try:
        driver_mod = importlib.import_module(driver_import)
    except ImportError as ierr:
        log.error('Unable to import from %s', driver_import)
        return napalm_driver
    class OpenConfigDriver(napalm_driver):
        pass
    for name, obj in inspect.getmembers(driver_mod):
        if name.startswith('openconfig_') and inspect.isfunction(obj):
            setattr(OpenConfigDriver, name, obj)
    return OpenConfigDriver

__all__ = ('get_network_driver', '__version__',)
