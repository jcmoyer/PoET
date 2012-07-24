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

import filecmp
import os

def add_parsers(parent):
  diff_parser = parent.add_parser('diff', help=('Provides a summary of what'
                                  'changed between two extraction versions'))
  diff_parser.add_argument('dir1', help='First (old) extraction directory')
  diff_parser.add_argument('dir2', help='Second (new) extraction directory')
  diff_parser.set_defaults(func=run)

def files_in(directory):
  base = None
  for (root, dirs, files) in os.walk(directory):
    if base is None: base = len(root) + 1
    for f in files:
      yield os.path.join(root, f)[base:]

def run(args):
  if not os.path.exists(args.dir1):
    print("The first directory provided does not exist.")
    return
  if not os.path.exists(args.dir2):
    print("The second directory provided does not exist.")
    return

  print('Comparing {0} to {1}...this will take some time.'.format(args.dir1,
                                                                  args.dir2))

  os.walk(args.dir1)
  (match, mismatch, errors) = filecmp.cmpfiles(args.dir1, args.dir2,
                                               files_in(args.dir2))

  for m in mismatch:
    print('MODIFIED {0}'.format(m))
  for e in errors:
    if not os.path.exists(os.path.join(args.dir1, e)):
      print('ADDED {0}'.format(e))
    elif not os.path.exists(os.path.join(args.dir2, e)):
      print('REMOVED {0}'.format(e))

