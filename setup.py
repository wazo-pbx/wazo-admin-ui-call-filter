#!/usr/bin/env python3
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from setuptools import find_packages
from setuptools import setup

setup(
    name='wazo_admin_ui_callfilter',
    version='0.1',

    description='Wazo Admin UI Callfilter',

    author='Wazo Authors',
    author_email='dev@wazo.community',

    url='http://wazo.community',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    entry_points={
        'wazo_admin_ui.plugins': [
            'callfilter = wazo_plugind_admin_ui_callfilter_official.plugin:Plugin',
        ]
    }
)
