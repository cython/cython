#!/usr/bin/env python
"""Wrapper to run setup.py using setuptools."""
import setuptools
with open('setup.py', 'rb') as f:
    exec(compile(f.read(), 'setup.py', 'exec'))
