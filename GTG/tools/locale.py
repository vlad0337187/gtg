import dataclasses
import locale
import os

import pydash


@dataclasses.dataclass
class LocaleInfo:
    language: str
    country : str
    encoding: str


def parse_locale(locale: str) -> LocaleInfo:
    """
    Parse locales of formats:
        - en_US.utf-8
        - en_US
        - en
    """
    lang_country_and_encoding = locale.split('.')
    lang_country              = lang_country_and_encoding[0]
    encoding                  = pydash.arrays.nth(lang_country_and_encoding, 1)
    lang_and_country          = lang_country.split('_')
    language                  = lang_and_country[0]
    country                   = pydash.arrays.nth(lang_and_country, 1)

    locale_info = LocaleInfo(language=language, country=country, encoding=encoding)
    return locale_info


def get_current_locale() -> LocaleInfo:
    language_and_country, encoding = locale.getlocale()
    locale_info                    = parse_locale(f'{language_and_country or "en_US"}.{encoding or "UTF-8"}')
    return locale_info
