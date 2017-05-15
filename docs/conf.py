#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# brpc documentation build configuration file

import alabaster

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'alabaster'
]

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# general project information
project = 'brpc'
copyright = '2017, Zack Buhman'
#version = brpc.__version__
#release = brpc.__version__

# styles
pygments_style = 'sphinx'
highlight_language = 'python3'

# The theme to use for HTML and HTML Help pages.
html_theme = 'alabaster'
html_theme_path = [alabaster.get_path()]

html_theme_options = {
    'description': 'buh rpc',
    'github_user': 'ptpb',
    'github_repo': 'brpc',
    'github_button': True,
    'github_type': 'star',
    'github_banner': True,
    'shield_list': [
        {
            'image': 'https://img.shields.io/circleci/project/github/ptpb/brpc.svg',
            'target': 'https://circleci.com/gh/ptpb/brpc'
        },
        {
            'image': 'https://img.shields.io/codecov/c/github/ptpb/brpc.svg',
            'target': 'https://codecov.io/gh/ptpb/brpc'
        },
        {
            'image': 'https://img.shields.io/pypi/v/brpc.svg',
            'target': 'https://pypi.org/project/brpc/'
        }
    ]
}

html_sidebars = {
    '**': [
        'about.html', 'navigation.html', 'searchbox.html',
    ]
}
