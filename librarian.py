import glob
import os
import re
from argparse import ArgumentParser

from print_utils import colprint

PROGRAM = 'Librarian'
DESCRIPTION = 'Video library name manager'

POSSIBLE_MOVIE_NAME_REGEX = r'^(?P<name>(\S+\.)*\S+)\.\S*(?P<year>\d{4})\S*(\d+p)\S*\.(?P<ext>mkv)$'
MOVIE_NAME_REGEX = r'^((\S+\ )*(\S+)) \(\d+\)\.mkv$'

if __name__ == '__main__':
    # Setup arguments
    parser = ArgumentParser(prog=PROGRAM, description=DESCRIPTION)
    parser.add_argument('--mode', choices=['check'], required=True)
    parser.add_argument('--print-follows', action='store_true', default=False)
    parser.add_argument('path')

    # Parse args
    args = parser.parse_args()
    mode = args.mode
    path = args.path

    if mode == 'check':
        colprint('|sbr|{} ({}) |cgr|CHECK MODE'.format(PROGRAM, DESCRIPTION))
        all_files = [entry for entry in glob.glob(path + '*', recursive=True) if not os.path.isdir(entry)]

        index = {'follows': [], '!follows': {'possible_applies': [], '!possible_applies': []}}

        colprint('Found total of |cgr||sbr|{}|rst| files in directory: |cgr||sbr|{}'.format(len(all_files), path))
        for path in all_files:
            filename = os.path.basename(path)

            match = re.match(MOVIE_NAME_REGEX, filename)

            if match is None:
                possible_match = re.match(POSSIBLE_MOVIE_NAME_REGEX, filename)
                if possible_match is None:
                    index['!follows']['!possible_applies'].append(path)
                else:
                    name = possible_match.group('name').replace('.', ' ')
                    year = possible_match.group('year')
                    ext = possible_match.group('ext')
                    possible_name = '{} ({}).{}'.format(name, year, ext)

                    index['!follows']['possible_applies'].append((path, possible_name))
            else:
                index['follows'].append(path)

        if len(index['follows']) > 0 and args.print_follows:
            colprint('|sbr|List of files that |cgr|follow |crst|naming rules:')
            for path in index['follows']:
                filename = os.path.basename(path)
                print(filename)
            print()

        if len(index['!follows']['possible_applies']):
            colprint('|sbr|List of files that |crd|don\'t follow |crst|naming rules, but |cgr|can be automatically '
                     'renamed|crst|:')
            for path, suggestion in index['!follows']['possible_applies']:
                filename = os.path.basename(path)
                colprint('|crd|{}|crst| -> |cgr|{}'.format(filename, suggestion))
            print()

        if len(index['!follows']['!possible_applies']):
            colprint('|sbr|List of files that |crd|don\'t follow |crst|naming rules and |crd|can\'t be automatically '
                     'renamed|crst|:')
            for path in index['!follows']['!possible_applies']:
                filename = os.path.basename(path)
                print(filename)
