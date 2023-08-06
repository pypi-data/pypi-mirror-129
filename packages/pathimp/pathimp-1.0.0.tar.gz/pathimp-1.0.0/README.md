[![PyPI](https://img.shields.io/pypi/v/pathimp.svg)](https://pypi.python.org/pypi/pathimp/#history) &nbsp;

# pathimp

Import Python modules from any file system path.

## Installation

```sh
pip3 install pathimp
```

## Usage

```python
import pathimp

pathimp.import_module(
    name='my_module',              # Name of the module directory or file.
    path='../path/to/parent/dir',  # Path or list of paths to search.
    notfound='error')              # Raise 'error' or 'ignore' when not found.

import my_module
```

## Details

After calling `pathimp.import_module()`, the module is available in
`sys.modules` and can be imported normally by later code. The function also
returns the module, allowing to use it directly without further import:

```python
import pathimp
my_module = pathimp.import_module('my_module', '../path/to/parent/dir')
```

If the module is not found as a directory or file under the provided path, a
`ModuleNotFoundError` is raied. The exception can be disable by passing the
`notfound='ignore'` argument:

```python
pathimp.import_module('my_module', '../path/to/parent/dir', notfound='ignore')
```

Whether the import succeeded can still be found out by looking at the return
value, which is either the module instance or `False` if the module was not
found.
