""" Initializes support for translations """

import i18n

from . import dirs

import GTG.tools.locale


def init():
    locale = GTG.tools.locale.get_current_locale()
    i18n.set('locale',   locale.language)
    i18n.set('fallback', 'en')
    i18n.config.settings['file_format']     = 'yaml'
    i18n.config.settings['filename_format'] = '{locale}.{format}'
    i18n.load_path.append(dirs.TRANSLATIONS_DIR)


def translate(phrase_single, count=None):
    if count:
        translated = i18n.t(phrase_single, count=count)
    else:
        translated = i18n.t(phrase_single)  # avoid pluralization, more fast

    return translated
