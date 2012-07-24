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

import argparse
import extract
import diff

parser = argparse.ArgumentParser(description='Path of Exile Tool')
subparsers = parser.add_subparsers()
extract.add_parsers(subparsers)
diff.add_parsers(subparsers)

def main():
  args = parser.parse_args()
  args.func(args)

if __name__ == '__main__':
  main()

