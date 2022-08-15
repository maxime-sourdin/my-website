#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
AUTHOR = 'Maxime SOURDIN'
EMAIL = 'maxime@sourdin.ovh'
SITENAME = 'Maxime SOURDIN'
SITESUBTITLE = ""
SITEURL_PUBLIC = 'https://maxime.sourdin.ovh'
SITEURL = 'https://maxime.sourdin.ovh'
SITEURL_LOCAL = 'https://maxime.sourdin.ovh'
PATH = 'content'
TIMEZONE = 'Europe/Paris'
AUTHOR_URL = 'author/{slug}'
AUTHOR_SAVE_AS = 'author/{slug}.html'
DEFAULT_LANG = 'fr'
DEFAULT_DATE_FORMAT = ('%b %d, %Y')
CATEGORY_SAVE_AS = '{slug}.html'
CATEGORY_URL = '{slug}'
TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}.html'
HIDE_AUTHORS = True
STATIC_PATHS = ['medias']
CC_LICENSE = 'CC-BY-SA'
ARTICLE_SAVE_AS = '{slug}.html'
ARTICLE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}.html'
PAGE_URL = '{slug}'
DEFAULT_DATE = None
DEFAULT_PAGINATION = 30
DIRECT_TEMPLATES = ['index']
LOAD_CONTENT_CACHE = False
REVERSE_ARCHIVE_ORDER = True
DISPLAY_PAGES_ON_MENU = False
THEME = 'themes/pelican-alchemy/alchemy'
THEME_CSS_OVERRIDES = ['theme/css/oldstyle.css']
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["sitemap", "pelican-redirect", "pelican-gitpython"]
SITEMAP = {
    'format': 'txt',
    'exclude': ['tag/', 'category/'],
    'changefreqs': {
        'articles': 'daily',
        'pages': 'monthly',
        'indexes': 'daily'
    }
}
LINKS = (
        ('CV', 'https://maxime.sourdin.ovh/cv'),
        ('CV (PDF)', 'https://maxime.sourdin.ovh/cv.pdf'),
        ('linkedin', 'https://linkedin.com/in/maxime-sourdin-15b082154'),
        ('email', 'mailto:maxime at sourdin.ovh'),
        ('github', 'https://github.com/maxime-sourdin'),
        ('blog', 'https://maxime.sourdin.ovh/author/maxime-sourdin')
        )
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.extra': {},
        'markdown.extensions.admonition': {},
        'markdown.extensions.codehilite': {
            'css_class': 'highlight'
        },
        'markdown.extensions.meta': {},
        'smarty' : {
            'smart_angled_quotes' : 'true'
        }
    }
}
