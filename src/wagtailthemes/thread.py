from threading import local

_thread_locals = local()


def set_theme(theme):
    setattr(_thread_locals, 'wagtail_theme', theme)


def get_theme():
    theme = getattr(_thread_locals, 'wagtail_theme', None)
    return theme
