#! /usr/bin/env python3


import os
import os.path as op


cur_dir   = op.dirname(__file__)
po_dir    = op.join(cur_dir, '../', 'po', 'pos')
all_files = os.listdir(po_dir)

all_po_files = [i for i in all_files if i.endswith('.po')]

for po_file in all_po_files:
	json_file = po_file.replace('.po', '.json')
	#os.system(f'node_modules/po2json/bin/po2json -t pos/en_GB.po --errorlevel traceback pos/{po_file} jsons/{json_file}')
	os.system(f'node_modules/po2json/bin/po2json --errorlevel traceback pos/{po_file} jsons/{json_file}')
