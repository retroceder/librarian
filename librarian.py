#!/usr/bin/python3

import glob
import os
import re
import sys
from argparse import ArgumentParser
from pathlib import PurePath as Path

import colorama
from colorama import Fore
from colorama import Style

# Program related constants
PROGRAM = 'Librarian'
DESCRIPTION = 'Video library name manager'

# Acknowledged file extensions
FILE_EXTENSIONS = {'mkv', 'mp4', 'avi', 'wmv'}
# Incorrect movie name regex (to enable autocorrection)
POSSIBLE_MOVIE_NAME_REGEX_LIST = [r'^(?P<name>(\S+\.)*\S+)\.(?P<year>\d{4})\S*(\d+p)\S*\.(?P<ext>' +
                                  '|'.join(FILE_EXTENSIONS) + ')$',
                                  r'^(?P<name>([^( ]+\ )*[^( ]+)\s\({0,1}(?P<year>\d{4})\({0,1}.*\.(?P<ext>' +
                                  '|'.join(FILE_EXTENSIONS) + ')$']
# Correct movie name regex
MOVIE_NAME_REGEX = r'^((\S+\ )*(\S+)) \(\d+\)\.mkv$'


# Process colprint formatted strings (replace colorama-specific symbols)
def colprocess(text: str):
    return text\
        .replace('|sbr|', Style.BRIGHT)\
        .replace('|sdm|', Style.DIM)\
        .replace('|rst|', Style.RESET_ALL)\
        .replace('|crst|', Fore.RESET)\
        .replace('|cgr|', Fore.GREEN)\
        .replace('|crd|', Fore.RED)


# Print specially formatted colored strings
def colprint(text: str):
    print(colprocess(text) + Style.RESET_ALL)


# Get file index for a given root path
def get_index(root_path: Path):
    all_files = [Path(entry) for entry in glob.glob('./*', root_dir=root_path, recursive=True) if not os.path.isdir(entry)]

    index = {'follows': [], '!follows': {'possible_applies': [], '!possible_applies': []}}

    colprint('Found total of |cgr||sbr|{}|rst| files in directory: |cgr||sbr|{}'.format(len(all_files), root_path))
    for relpath in all_files:
        filename = os.path.basename(root_path / relpath)

        match = re.match(MOVIE_NAME_REGEX, filename)

        if match is None:
            matched = False
            for possible_regex in POSSIBLE_MOVIE_NAME_REGEX_LIST:
                possible_match = re.match(possible_regex, filename)
                if possible_match is not None:
                    name = possible_match.group('name').replace('.', ' ')
                    year = possible_match.group('year')
                    ext = possible_match.group('ext')
                    possible_name = '{} ({}).{}'.format(name, year, ext)

                    index['!follows']['possible_applies'].append((root_path / relpath, possible_name))

                    matched = True
                    break

            if not matched:
                index['!follows']['!possible_applies'].append(root_path / relpath)
        else:
            index['follows'].append(root_path / relpath)

    return index


# Entry point
if __name__ == '__main__':
    # Initialization
    colorama.init()

    # Setup arguments
    parser = ArgumentParser(prog=PROGRAM, description=DESCRIPTION)
    parser.add_argument('--mode', choices=['check', 'correct'], required=True)
    parser.add_argument('--print-follows', action='store_true', default=False)
    parser.add_argument('path')

    # Parse args
    args = parser.parse_args()
    mode = args.mode
    path = Path(args.path)

    if mode == 'check':
        colprint('|sbr|{} ({}) |cgr|CHECK MODE'.format(PROGRAM, DESCRIPTION))

        index = get_index(path)

        # Print file index
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

    if mode == 'correct':
        colprint('|sbr|{} ({}) |cgr|CORRECTION MODE'.format(PROGRAM, DESCRIPTION))

        index = get_index(path)

        if len(index['!follows']['possible_applies']):
            colprint('|sbr|List of files that |crd|don\'t follow |crst|naming rules, but |cgr|can be automatically '
                     'renamed|crst|:')
            for path, suggestion in index['!follows']['possible_applies']:
                filename = os.path.basename(path)
                colprint('|crd|{}|crst| -> |cgr|{}'.format(filename, suggestion))
            print()

            proceed = None
            while proceed is None:
                ans = input('Do you wish to proceed? (Y/N): ')

                if ans == 'Y':
                    proceed = True
                if ans == 'N':
                    proceed = False

            if not proceed:
                colprint('|sbr||crd|Abort.')
                sys.exit(1)

            for path, suggestion in index['!follows']['possible_applies']:
                filename = os.path.basename(path)
                colprint('Renaming |crd|{}|crst| -> |cgr|{}'.format(filename, suggestion))
                os.rename(path, path.parent / suggestion)

        else:
            colprint('|sbr||crd|There are no files that can be automatically corrected.')
