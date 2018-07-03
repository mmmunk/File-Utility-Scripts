#!python3

# Version 0.5 - 2017-12-20 - Thomas Munk

import os
import argparse
import hashlib
from collections import defaultdict

parser = argparse.ArgumentParser(description='Searches a folder for multiple occurrences of the same file')
parser.add_argument('-r', '--recursive', help='Search recursively into subfolders', action='store_true')
parser.add_argument('-o', '--output', help='Output result to a file', type=str)
#TODO: include/exclude file-wildcards, include/exclude file-paths
parser.add_argument('path', help='Relative or full path to search for doublets', type=str)
args = parser.parse_args()

if not os.path.isdir(args.path):
	print(args.path, 'is not a directory')
	exit(1)

#TODO: create output file
#TODO: write args to file

hash_dict = defaultdict(list)

def file_hash(file):
	sha1 = hashlib.sha1()
	with open(file, 'rb') as f:
		while True:
			buf = f.read(512*1024)
			if not buf:
				break
			sha1.update(buf)
	return sha1.hexdigest()

def search_single_folder(folder):
	print(folder)
	try:
		file_names = os.listdir(folder)
	except:
		#TODO: also in output file:
		print('Error opening folder:', folder)
		return
	dir_names = []
	for fn in file_names:
		fn = os.path.join(folder, fn)
		if os.path.isfile(fn):
			try:
				hash_dict[file_hash(fn)].append(fn)
			except:
				#TODO: also in output file:
				print('Error opening file:', fn)
		elif args.recursive and os.path.isdir(fn):
			dir_names.append(fn)
	dir_names.sort(key=str.lower)
	for fn in dir_names:
		search_single_folder(fn)

print('Searching...')
search_single_folder(args.path)

total = 0
for hash_key, file_names in hash_dict.items():
	count = len(file_names)
	if count > 1:
		total += 1
		#TODO: output file
		print()
		print(count, 'doublets:')
		for fn in file_names:
			print(fn)
#TODO: both screen and output file:
print()
print('Unique files with doublets:', total)