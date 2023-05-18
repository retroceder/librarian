# Librarian
A script for checking and enforcing video library file naming convention.

## Prerequisites
- Python (>=3.8)

## Build and installation
To build package, run:
```shell
python setup.py bdist_wheel
```

Resulting redistributable `.whl` package will be in `dist` directory.

To install package, run:
```shell
python -m pip install librarian-<version>-py3-none-any.whl
```

## Usage
### Check mode (no action)
To run naming convention check:
```shell
librarian --mode check <path>  # path - root directory of video library
```

By default, the script doesn't print filenames that follow naming convention. This can be changed by running:
```shell
librarian --mode check --print-follows <path>  # path - root directory of video library
```

### Correction mode
To enforce naming convention (i.e. automatically rename files), run:
```shell
librarian --mode correct <path>  # path - root directory of video library
```
