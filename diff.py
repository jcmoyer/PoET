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

  os.walk(args.dir1)
  (match, mismatch, errors) = filecmp.cmpfiles(args.dir1, args.dir2, files_in(args.dir2))

  for m in mismatch:
    print('MODIFIED {0}'.format(m))
  for e in errors:
    if not os.path.exists(os.path.join(args.dir1, e)):
      print('ADDED {0}'.format(e))
    elif not os.path.exists(os.path.join(args.dir2, e)):
      print('REMOVED {0}'.format(e))

