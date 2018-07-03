#!python3

# Version 1.0.0 - 2017-12-29 - Thomas Munk
# Version 1.0.1 - 2018-01-05 - Thomas Munk
# Uses Pillow (PIL - Python Imaging Library): pip install pillow

import os
import argparse
from datetime import datetime, timedelta
from PIL import Image

# Returns a datetime object if dt string is a correctly formatted exif date/time
def parse_exif_datetime(dt):
	try:
		if ':' == dt[4] == dt[7] == dt[13] == dt[16]:
			return datetime(year=int(dt[:4]), month=int(dt[5:7]), day=int(dt[8:10]), hour=int(dt[11:13]), minute=int(dt[14:16]), second=int(dt[17:]))
		else:
			return None
	except:
		return None

# Parse arguments
parser = argparse.ArgumentParser(description='Rename JPEG picture files to their internal EXIF date/time')
parser.add_argument('-n', '--rename', help='Rename files instead of showing filenames', action='store_true')
parser.add_argument('--offset', help='Offset in minutes (positive or negative) that will be added to date/time found in files', type=int, default=0)
parser.add_argument('--allfiles', help='Include all files instead of only files with JPEG extension', action='store_true')
parser.add_argument('path', help='Relative or full path to a folder with picture files', type=str)
args = parser.parse_args()

# Path argument must be a directory
if not os.path.isdir(args.path):
	print(args.path, 'is not a directory')
	exit(1)

# Build list of files to process
src_names = []
for fn in os.listdir(args.path):
	pfn = os.path.join(args.path, fn)
	if os.path.isfile(pfn) and not os.path.islink(pfn):
		if args.allfiles or os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg'):
			src_names.append(fn)
if not src_names:
	print('No files found')
	exit(2)
src_names.sort(key=str.lower)

# Find longest filename
fn_len = 0
for fn in src_names:
	n = len(fn)
	if n > fn_len:
		fn_len = n
if fn_len > 50:
	fn_len = 50

# Process each file
for fn in src_names:
	print(fn.ljust(fn_len), '   ', end='')
	pfn = os.path.join(args.path, fn)
	# Try to extract EXIF DateTimeOriginal string from file
	try:
		dtstr = Image.open(pfn)._getexif()[0x9003]
	except:
		dtstr = None
	if dtstr:
		# Parse EXIF string
		dtobj = parse_exif_datetime(dtstr)
		if dtobj:
			# Add a possible minute-offset
			if args.offset:
				dtobj += timedelta(minutes=args.offset)
			# Generate new date/time filename
			dtfn = dtobj.strftime('%Y-%m-%d %H.%M.%S')+os.path.splitext(fn)[1].lower()
			if dtfn == fn:
				print('OK')
			else:
				if args.rename:
					# Rename file
					pdtfn = os.path.join(args.path, dtfn)
					if os.path.isfile(pdtfn):
						print('File exists:', dtfn)
					else:
						try:
							os.rename(pfn, pdtfn)
							print('Renamed to', dtfn)
						except:
							print('Rename error:', dtfn)
				else:
					# Only display new filename
					print(dtfn)
		else:
			print('Invalid tag:', dtstr)
	else:
		print('No tag')