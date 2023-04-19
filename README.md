# Librarian
A script for checking video library file naming convention.

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
