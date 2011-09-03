#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Py2Exe setup script'''

from distutils.core import setup
import py2exe

setup(  options = {
                  "py2exe":
                            {
                             "compressed": 1, 
                             "optimize": 2, 
                             "bundle_files": 1,
                             "dll_excludes": [ "mswsock.dll", "powrprof.dll" ]
                             }
                 },

        zipfile = None,
        console = [{"script":"fakesmtp.py"}] 
    )
