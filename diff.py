#   Copyright 2012 J.C. Moyer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import sys

# File comparison constants
Same     = 0
Modified = 1
New      = 2
Deleted  = 3

def add_parsers(parent):
  diff_parser = parent.add_parser('diff', help=('Provides a summary of what '
                                  'changed between two extraction versions'))
  diff_parser.add_argument('dir1', help='First (old) extraction directory')
  diff_parser.add_argument('dir2', help='Second (new) extraction directory')
  diff_parser.add_argument('-bs',
                           help=('Size of buffer to use when comparing files '
                                 '(default 16383)'),
                           type=int, dest='buffersize', default=0x3FFF,
                           metavar='size')
  diff_parser.add_argument('-f',
                           help='Filename to optionally write results to',
                           type=str, dest='filename', default=None,
                           metavar='filename')
  diff_parser.set_defaults(func=run)

def tree(directory, child_base=True):
  """
  Given a directory, returns each file in the directory and its subdirectories
  recursively.
  """
  base = 0
  for (root, dirs, files) in os.walk(directory):
    if child_base and base is 0: base = len(root) + 1
    for f in files:
      yield os.path.join(root, f)[base:]

def compare(f1, f2, bufsize=0x3FFF):
  """
  Given two filenames, compares the files and returns a value representing the
  difference.

  Keyword arguments:
    bufsize -- size of buffer to use when comparing files. Defaults to 0x3FFF,
    which is 16K.

  Returns one of the constants:
    * Same
    * Modified
    * New
    * Deleted
  """
  f1_exists = os.path.exists(f1)
  f2_exists = os.path.exists(f2)
  if not f1_exists and f2_exists:
    return New
  if f1_exists and not f2_exists:
    return Deleted
  if os.path.getsize(f1) != os.path.getsize(f2):
    return Modified
  with open(f1, 'rb') as fd1, open(f2, 'rb') as fd2:
    while True:
      chunk1 = fd1.read(bufsize)
      chunk2 = fd2.read(bufsize)
      if chunk1 != chunk2: return Modified
      # If the files both end at the same place then break.
      if not chunk1 and not chunk2:
        break
  return Same

def diff(d1, d2, bufsize=0x3FFF, fd=None):
  """
  Recursively compares the files contained in two directories and prints
  information about what changed.

  Keyword arguments:
    bufsize -- size of buffer to use when comparing files. Defaults to 0x3FFF,
    which is 16K.
    fd -- file descriptor to write summaries to in addition to stdout.
  """
  t1 = tree(d1)
  t2 = tree(d2)
  for f in t2:
    result = compare(os.path.join(d1, f), os.path.join(d2, f), bufsize)
    if result == New:
      write_summary_item('NEW', f, sys.stdout, fd)
    elif result == Modified:
      write_summary_item('MODIFIED', f, sys.stdout, fd)
    elif result == Deleted:
      write_summary_item('DELETED', f, sys.stdout, fd)

def write_summary_item(kind, item, *files):
  for f in files:
    if f:
      f.write("{0:10}{1}{2}".format(kind, item, os.linesep))

def run(args):
  if not os.path.exists(args.dir1):
    print("The first directory provided does not exist.")
    return
  if not os.path.exists(args.dir2):
    print("The second directory provided does not exist.")
    return

  print('Comparing {0} to {1}...this will take some time.'.format(args.dir1,
                                                                  args.dir2))

  if args.filename is not None:
    with open(args.filename, 'w+') as f:
      diff(args.dir1, args.dir2, args.buffersize, f)
  else:
    diff(args.dir1, args.dir2, args.buffersize)
