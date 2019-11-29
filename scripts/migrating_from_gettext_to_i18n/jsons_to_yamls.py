#! /usr/bin/env python3

import json
import pathlib as p
import re

import yaml


REGEXP_COUNT_STR = '''
	\%\(    # exact match to: %(
	.*      # any character 0 or more times
	\)      # close brace: )
	\S*     # not space character 0 or more times
'''
REGEXP_COUNT = re.compile(REGEXP_COUNT_STR, re.VERBOSE)

REGEXP_COUNT_TO_EXTRACT_VALUES_STR = '''
	\%\(    # exact match to: %(
	(       # group 1
	.*      # any character 0 or more times
	)       # group 1 end
	\)      # close brace: )
	(       # group 2
	\S*     # not space character 0 or more times
	)       # group 2 end
'''
REGEXP_COUNT_TO_EXTRACT_VALUES = re.compile(REGEXP_COUNT_TO_EXTRACT_VALUES_STR, re.VERBOSE)


def get(obj, key_or_index):
	try:
		return obj[key_or_index]
	except (KeyError, IndexError):
		return None


def convert_formatted_strings_from_old_to_new_format(string_old):
	"""
	Convert earlier met Python formatted strings to `python-i18n` format.
	Earlier examples:
		%(tasks)d
		%(days)d
		%(task_title)s
	New examples:
		...
	"""
	match_obj   = re.search(REGEXP_COUNT_TO_EXTRACT_VALUES, string_old)
	word_inside = match_obj.group(1)
	ending      = match_obj.group(2)
	string_new = '%{' + word_inside + '}' + ending
	return string_new


def convert_json_translations_into_python_i18n_format(translation_source: dict, lang: str) -> dict:
	result = {lang: {}}

	for item, translations in translation_source.items():
		translations_fixed = []

		is_technical_info = isinstance(translations, dict)
		if is_technical_info:
			continue

		# fix substitutions in item
		if '%(' in item:
			item = convert_formatted_strings_from_old_to_new_format(item)

		# fix substitutions in translations
		for translation in translations:
			# special case handling (don't know why it's happened)
			if isinstance(translation, list):
				translation = translation[0]

			if translation and '%(' in translation:
				substitutions_old = REGEXP_COUNT.findall(translation)

				for substitution_old in substitutions_old:
					substitution_new = convert_formatted_strings_from_old_to_new_format(substitution_old)
					translation = translation.replace(substitution_old, substitution_new)

			translations_fixed.append(translation)

		# translations examples:
		#		['%(days)d days ago', 'Вчора', '%(days)d дні тому', '%(days)d днів тому']
		#		[' minutes', ' minute', ' minutes']
		#		[None, 'завтра']

		form_one           = get(translations_fixed, 1)
		form_many          = get(translations_fixed, 2)
		form_many_original = get(translations_fixed, 0)

		if form_one and not form_many:
			result[lang][item] = form_one
		else:
			result[lang][item]         = {}
			result[lang][item]['one']  = form_one
			result[lang][item]['many'] = form_many

		if form_many_original:
			result[form_many_original] = result[lang][item]

	return result


def main():
	current_dir	= p.Path(__file__).parent
	dir_jsons	= current_dir / 'jsons'		# source translations
	dir_yamls	= current_dir / 'yamls'		# ready translations
	files_json	= [f for f in dir_jsons.iterdir() if f.is_file() and f.name.endswith('.json')]

	for file_json in files_json:
		#if not file_json.name == 'ru.json':
		#	continue

		with open(file_json, 'tr') as file:
			translation_source_json	= file.read()

		file_ready_name	 = file_json.name.replace('.json', '.yaml')
		file_ready_path	 = dir_yamls / file_ready_name
		lang_and_country = file_json.name.replace('.json', '')  # 'en_US', 'en', 'ru_RU'
		lang             = lang_and_country.split('_')[0]

		translation_source_dict	= json.loads(translation_source_json)
		translation_ready_dict	= convert_json_translations_into_python_i18n_format(translation_source_dict, lang)
		translation_ready_yaml	= yaml.dump(translation_ready_dict, default_flow_style=False, allow_unicode=True, indent=4)



		with open(file_ready_path, 'tw') as file_yaml:
			file_yaml.write(translation_ready_yaml)


if __name__ == '__main__':
	main()
