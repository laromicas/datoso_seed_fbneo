"""
__init__.py
"""
__all__ = ["__version__", "__author__", "__description__"]
__version__ = "0.0.1"
__author__ = "Lacides Miranda"
__description__ = "Datoso plugin for seed Final Burn Neo"
__preffix__ = "fbneo"

from datoso.configuration import config
if not config.has_section('FBNEO'):
    config['FBNEO'] = {
        'FetchFull': True,
        'FetchLight': False,
    }