# Librarian
A script for checking and enforcing video library file naming convention.

## Usage
### Check mode (no action)
To run naming convention check:
```sh
python librarian.py --mode check <path>  # path - root directory of video library
```

By default script doesn't print filenames that follow naming convention. This can be changed by running:
```sh
python librarian.py --mode check --print-follows <path>  # path - root directory of video library
```

## Usage
### Correction mode
To enforce naming convention (i.e. automatticaly rename files), run:
```sh
python librarian.py --mode correct <path>  # path - root directory of video library
```
