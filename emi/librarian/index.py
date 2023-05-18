import re
import glob
import os
from pathlib import PurePath as Path


def get_index(root_path: Path, movie_regex: str, possible_movie_regex: list):
    """Get file index for a given root path."""
    all_files = [Path(entry) for entry in glob.glob(str(root_path) + '/*', recursive=True)
                 if not os.path.isdir(root_path / entry)]

    index = {'follows': [], '!follows': {'possible_applies': [], '!possible_applies': []}}
    total_files = len(all_files)

    for relpath in all_files:
        filename = os.path.basename(root_path / relpath)

        match = re.match(movie_regex, filename)

        if match is None:
            matched = False
            for possible_regex in possible_movie_regex:
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

    return index, total_files
