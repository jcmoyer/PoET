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
import ggpk

def add_parsers(parent):
  extract_parser = parent.add_parser('extract', help='Extracts a .ggpk file')
  extract_parser.add_argument('filename', help='Path to .ggpk file')
  extract_parser.add_argument('directory', help='Directory to extract files to')
  extract_parser.set_defaults(func=run)

def extract_recurse(arch, dest, path, item):
  destname = os.path.join(dest, path, item.name)
  if isinstance(item, ggpk.DirectoryEntry):
    print('Extracting directory ' + destname)
    if not os.path.exists(destname):
      os.mkdir(destname)
    for child in item.children:
      extract_recurse(arch, dest, os.path.join(path, item.name), child)
  elif isinstance(item, ggpk.FileEntry):
    with open(destname, 'wb+') as f:
      data = arch.extract(item)
      f.write(data)

def run(args):
  if not os.path.exists(args.filename):
    print(args.filename + ' does not exist')
    return

  with ggpk.File(args.filename) as archive:
    extract_recurse(archive, args.directory, '', archive.root())

  print('Done.')
