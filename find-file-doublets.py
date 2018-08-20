#!/usr/bin/env python3

# Posix and Windows
# Version 1.0 - 2018-08-20 - Thomas Munk

import sys
import os
import argparse
import hashlib
from collections import defaultdict
from fnmatch import fnmatch

hash_dict = defaultdict(list)

def file_hash(fn):
	sha1 = hashlib.sha1()
	with open(fn, 'rb') as f:
		while True:
			buf = f.read(512*1024)
			if not buf:
				break
			sha1.update(buf)
	return sha1.hexdigest()

def process_dir(path):
	if args.verbose:
		print('[', path, ']', file=sys.stderr, flush=True)
	try:
		files = os.listdir(path)
	except:
		print('Error opening directory:', path)
		return
	dirs = []
	for fn in files:
		fn = os.path.join(path, fn)
		if os.path.isfile(fn):
			try:
				hash_dict[file_hash(fn)].append(fn)
			except OSError:
				print('Error opening file:', fn)
		elif args.recursive and os.path.isdir(fn):
			dirs.append(fn)
	dirs.sort(key=str.lower)
	for fn in dirs:
		process_dir(fn)

parser = argparse.ArgumentParser(description='Searches a number of paths for multiple occurrences of the same files')
parser.add_argument('-r', '--recursive', action='store_true', help='Include subdirectories')
parser.add_argument('-v', '--verbose', action='store_true', help='Output all directory names for progress purpose')
parser.add_argument('--match', metavar='PATTERN', type=str, help='Output a list of doublet files matching shell style wildcards in PATTERN')
parser.add_argument('--matchnot', action='store_true', help='Change the output of match list to doublet files not matching PATTERN')
parser.add_argument('--matchout', metavar='STRING', type=str, help='Format output of match list. Include FILENAME as placeholder for doublet file in STRING')
parser.add_argument('path', nargs='+', help='A number of paths to search for doublet files', type=str)
args = parser.parse_args()

# Validate arguments
for fn in args.path:
	if not os.path.isdir(fn):
		print(fn, 'is not a directory', file=sys.stderr)
		exit(1)
if args.matchout and args.matchout.count('FILENAME') < 1:
	print('A least one placeholder string FILENAME must exist in matchout string', file=sys.stderr)
	exit(2)

# Generate a hash for all files in all paths
if not args.verbose:
	print('Please wait, reading all files...', file=sys.stderr, flush=True)
for fn in args.path:
	process_dir(fn)

# Print doublet files and generate match list
match_files = []
total = 0
for key, files in hash_dict.items():
	count = len(files)
	if count > 1:
		total += 1
		print()
		print(count, 'doublets:')
		for fn in files:
			print(fn)
			if args.match:
				if fnmatch(fn, args.match) != args.matchnot:
					match_files.append(fn)
print()
print('Unique files with doublets:', total)

# Print match list
if args.match:
	print()
	print('Match list:')
	if match_files:
		match_files.sort(key=str.lower)
		for fn in match_files:
			if args.matchout:
				print(args.matchout.replace('FILENAME', fn))
			else:
				print(fn)
	else:
		print('(empty)')
