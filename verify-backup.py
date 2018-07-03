#!/usr/bin/python3

# Posix and Windows
# Version 0.9, Python 3.6, 2018-07-03, Thomas Munk

import sys
import os
import argparse
from fnmatch import fnmatch

FILE_CHUNK_SIZE = 512*1024


def file_content_diff(fno, fnb):

	with open(fno, 'rb') as f1:
		with open(fnb, 'rb') as f2:
			while True:
				b1 = f1.read(FILE_CHUNK_SIZE)
				b2 = f2.read(FILE_CHUNK_SIZE)
				if not b1 and not b2:
					return False
				if b1 != b2:
					return True


def compare_dir_level(common_path):

	ok = True
	diro = os.path.join(args.original_dir, common_path)
	dirb = os.path.join(args.backup_dir, common_path)
	if args.verbose:
		print('[', common_path, ']')
		sys.stdout.flush()

	# Read original directory - exceptions are valid reason to stop
	diro_files = set()
	diro_dirs = set()
	for fn in os.listdir(diro):
		if not args.exclude_patterns or	all([not fnmatch(fn, pt) for pt in args.exclude_patterns]):
			fno = os.path.join(diro, fn)
			if os.path.isfile(fno):
				diro_files.add(fn)
			elif os.path.isdir(fno):
				diro_dirs.add(fn)

	# Read backup directory - exceptions are valid reason to stop
	dirb_files = set()
	dirb_dirs = set()
	for fn in os.listdir(dirb):
		if not args.exclude_patterns or	all([not fnmatch(fn, pt) for pt in args.exclude_patterns]):
			fnb = os.path.join(dirb, fn)
			if os.path.isfile(fnb):
				dirb_files.add(fn)
			elif os.path.isdir(fnb):
				dirb_dirs.add(fn)

	# Missing files in backup directory
	for fn in sorted(diro_files - dirb_files, key=str.lower):
		ok = False
		print('File', os.path.join(diro, fn), 'does not exist in backup directory', dirb, file=sys.stderr)

	# Missing directories in backup directory
	for fn in sorted(diro_dirs - dirb_dirs, key=str.lower):
		ok = False
		print('Directory', os.path.join(diro, fn), 'does not exist in backup directory', dirb, file=sys.stderr)

	# Missing files in original directory
	for fn in sorted(dirb_files - diro_files, key=str.lower):
		ok = False
		print('Backup file', os.path.join(dirb, fn), 'does not exist in directory', diro, file=sys.stderr)

	# Missing directories in original directory
	for fn in sorted(dirb_dirs - diro_dirs, key=str.lower):
		ok = False
		print('Backup directory', os.path.join(dirb, fn), 'does not exist in directory', diro, file=sys.stderr)

	# File differences
	for fn in sorted(diro_files & dirb_files, key=str.lower):
		fno = os.path.join(diro, fn)
		fnb = os.path.join(dirb, fn)
		try:
			stato = os.stat(fno)
			statb = os.stat(fnb)
			if stato.st_size != statb.st_size:
				ok = False
				print('File', fno, 'and backup file', fnb, 'have different sizes', file=sys.stderr)
			elif file_content_diff(fno, fnb):
				ok = False
				print('File', fno, 'and backup file', fnb, 'have different content', file=sys.stderr)
			elif args.timediff and abs(stato.st_mtime - statb.st_mtime) >= 2.0:
				print('File', fno, 'and backup file', fnb, 'have different modification times', file=sys.stderr)
		except OSError as errobj:
			ok = False
			print('Error reading file', errobj.filename, errobj, file=sys.stderr)

	# Recursive traversal of common directories
	if args.recursive:
		for fn in sorted(diro_dirs & dirb_dirs, key=str.lower):
			ok = compare_dir_level(os.path.join(common_path, fn)) and ok

	# Flush and return combined result
	sys.stderr.flush()
	return ok


# Parse arguments
parser = argparse.ArgumentParser(description=
	'This utility will read all files from a backup and compare them to the original files. '
	'Non-identical, missing or excess files will be reported. '
	'A successful run will verify that all files are in a readable condition. '
	'File system errors will be reported. '
	'All filename comparisons are case sensitive.')
parser.add_argument('-r', '--recursive', help='Include subdirectories', action='store_true')
parser.add_argument('-t', '--timediff', help='Report if modification time differs for identical files', action='store_true')
parser.add_argument('-v', '--verbose', help='Output all directory names for progress purpose', action='store_true')
parser.add_argument('-x', help='Quoted wildcards for file or directory exclusion', action='append', type=str, metavar='pattern', dest='exclude_patterns')
parser.add_argument('original_dir', help='Original directory', type=str)
parser.add_argument('backup_dir', help='Backup directory', type=str)
args = parser.parse_args()

# Check for directory existence
if not os.path.isdir(args.original_dir) or not os.path.isdir(args.backup_dir):
	print('Both original and backup directory must exist')
	exit(1)

# Do the comparison
print('Comparing directory', args.original_dir, 'with backup directory', args.backup_dir, file=sys.stderr)
if compare_dir_level(''):
	print('Success: All files was read and compared without problems', file=sys.stderr)
else:
	exit(2)