# Wagtail-themes

Site specific theme loader for Django Wagtail.

[![Build Status](https://travis-ci.org/moorinteractive/wagtail-themes.svg?branch=master)](https://travis-ci.org/moorinteractive/wagtail-themes)
[![Coverage Status](https://coveralls.io/repos/github/moorinteractive/wagtail-themes/badge.svg?branch=master)](https://coveralls.io/github/moorinteractive/wagtail-themes?branch=master)

* Issues: [https://github.com/moorinteractive/wagtail-themes/issues](https://github.com/moorinteractive/wagtail-themes/issues)
* Testing: [https://travis-ci.org/moorinteractive/wagtail-themes](https://travis-ci.org/moorinteractive/wagtail-themes)
* Coverage: [https://coveralls.io/github/moorinteractive/wagtail-themes](https://coveralls.io/github/moorinteractive/wagtail-themes)

## Example app

See the [example](https://github.com/moorinteractive/wagtail-themes/tree/master/example) app for a working multisite with two different themes.

Run `make` and the app will install all the necessary files and fixtures for you. You can login with `admin:admin` and check how `example.com` and `blog.example.com` serve different themes.

## Installation

Install the package

```
pip install wagtail-themes
```

Add `wagtailthemes` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'wagtailthemes',
]
```

Add `ThemeMiddleware` to your `MIDDLEWARE_CLASSES` and make sure its added
after `SiteMiddleware`

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    'wagtailthemes.middleware.ThemeMiddleware',
]
```

Now make sure the `ThemeLoader` is added to your `loaders` config in the setting
`TEMPLATES`. Note that Django by default adds `APP_DIRS` to the setting, which
conflicts with defining your custom `loaders` config.

Also note that the `ThemeLoader` must be placed on the top of the list
(otherwise default templates will be found first).

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        # Remove 'APP_DIRS': True at this position
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'wagtailthemes.loaders.ThemeLoader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]
```

Now select where your themes are stored with the `WAGTAIL_THEME_PATH` settings
which has a default value of `None`.

```python
WAGTAIL_THEME_PATH = 'themes'
```

Note that the setting `WAGTAIL_THEME_PATH` is optional. We strongly recommend
using this if you have a large set of themes to keep your template directory
maintainable.

Finally define your to be used themes in the setting `WAGTAIL_THEMES`

```python
WAGTAIL_THEMES = [
    ('brand', 'Brand site'),
    ('personal', 'Personal site')
]
```

## ThemeLoader

The `ThemeLoader` class searches for files in your (see settings above) defined
`DIRS` config for `TEMPLATES`.

In this case templates files will be found in the following order (for this
example code we have set `brand` as theme in our CMS)

1. /myapp/templates/themes/brand/
2. /myapp/templates/

Its wise to build your templates as you are used to and only override the
template files you want to customize in your theme.

## theme_static tag

Works just like the standard Django `static` tag, but when a theme is active,
it will also prefix the theme path.  E.g. If the theme `brand` is active
`{% theme_static img/logo.png %}` will give /static/theme/brand/img/logo.png
If no theme was active it'd just be /static/img/logo.png

```python
{% load theme_static %}

<link rel="apple-touch-icon-precomposed" sizes="144x144" href="{% theme_static 'img/favicon-144x144.png' %}" />
```
