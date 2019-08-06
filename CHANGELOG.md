## [0.3.0] - 2019-08-06
### Fixed
* Compatibility for Django 2.x and Wagtail 2.x

### Removed
* Support for Django 1.x and Wagtail 1.x


## [0.2.0] - 2016-11-30
### Fixed
* Verbose name of `themes` instead of `Theme settings`
* Exception `ImproperlyConfigured` in `ThemeMiddleware`

### Added
* Optional settings `WAGTAIL_THEME_PATH` for storing themes into one directory (issue [#5])
* Unit and integration tests and CI with Travis

## [0.1.3] - 2016-09-12
### Fixed
* Backwards compatibility with Django 1.10 new middleware classes (issue [#1])

## [0.1.2] - 2016-09-12
### Fixed
* Missing README.md when installing from pypi

## [0.1.1] - 2016-09-12
### Fixed
* Prevent making migrations when changing `WAGTAIL_THEMES` (issue [#2])

## 0.1.0 - 2016-09-09
### Added
* Initial prototype

[0.2.0]: https://github.com/moorinteractive/wagtail-themes/compare/0.1.3...0.2.0
[0.1.3]: https://github.com/moorinteractive/wagtail-themes/compare/0.1.2...0.1.3
[0.1.2]: https://github.com/moorinteractive/wagtail-themes/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/moorinteractive/wagtail-themes/compare/0.1...0.1.1
[#5]: https://github.com/moorinteractive/wagtail-themes/issues/5
[#2]: https://github.com/moorinteractive/wagtail-themes/issues/2
[#1]: https://github.com/moorinteractive/wagtail-themes/issues/1
