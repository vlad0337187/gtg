import locale
import logging
import os
import _bootlocale

import pydash

from . import core
from . import tools


def main():
    setup_locale()
    ensure_utf8_is_default_encoding_for_open_function()
    core.translations.init()


def setup_locale():
    locale_                   = os.environ['LANG'] or os.environ['LANGUAGE']
    locale_info               = tools.locale.parse_locale(locale_)
    is_utf8                   = locale_info.encoding in ['utf-8', 'UTF-8', 'utf8', 'utf8']
    locale_                   = f'{locale_info.language}_{locale_info.country}.UTF-8'
    locale_supported_in_linux = 'en_US.utf-8'

    for locale_to_install in [locale_, locale_supported_in_linux, '', 'C']:
        try:
            locale.setlocale(locale.LC_ALL, locale_to_install)
            break
        except locale.Error as err:
            logging.error(f'unsupported locale: {locale_to_install}')


def ensure_utf8_is_default_encoding_for_open_function():
    """
    Not always locales are supported, sometimes `open()`, which uses `locale.getpreferredencoding`,
    defaults to ansi, which leads to errors.
    """
    is_utf8_in_bootlocale = _bootlocale.getpreferredencoding(False)
    is_utf8_in_locale     = locale     .getpreferredencoding(do_setlocale=False)

    def return_utf8_locale(do_setlocale=False):  # ignore setting locale
        return 'utf-8'

    if not is_utf8_in_bootlocale:
        _bootlocale.getpreferredencoding = return_utf8_locale
    if not is_utf8_in_locale:
        locale.getpreferredencoding = return_utf8_locale
