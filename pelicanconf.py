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
DEFAULT_LANG = 'fr'
DEFAULT_DATE_FORMAT = ('%b %d, %Y')
CATEGORY_SAVE_AS = '{slug}.html'
CATEGORY_URL = '{slug}.html'
FEED_ATOM = 'atom.xml'
HIDE_AUTHORS = True
RSS_FEED_SUMMARY_ONLY = True
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_DOMAIN = SITEURL
STATIC_PATHS = ['medias']
CC_LICENSE = 'CC-BY-SA'
ARTICLE_SAVE_AS = '{slug}.html'
ARTICLE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
PAGE_URL = '{slug}.html'
DEFAULT_DATE = None
DEFAULT_PAGINATION = 30
DIRECT_TEMPLATES = ['index']
LOAD_CONTENT_CACHE = False
REVERSE_ARCHIVE_ORDER = True
DISPLAY_PAGES_ON_MENU = False
THEME = 'themes/pelican-alchemy/alchemy'
THEME_CSS_OVERRIDES = ['theme/css/oldstyle.css']
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["sitemap"]
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
        ('linkedin', 'https://linkedin.com/in/maxime-sourdin-15b082154'),
        ('email', 'mailto:maxime at sourdin.ovh'),
        ('gitlab', 'https://gitlab.com/maximesrd'),
        ('feed', 'https://maxime.sourdin.ovh/atom.xml'),
        ('blog', 'https://maxime.sourdin.ovh/author/maxime-sourdin.html')
        )
