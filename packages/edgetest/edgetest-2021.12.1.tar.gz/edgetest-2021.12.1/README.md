# Bleeding edge dependency testing

![python-3.7](https://img.shields.io/badge/python-3.7-green.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[Full Documentation](https://capitalone.github.io/edgetest/)

`edgetest` is a `tox`-inspired python library that tests your package against the latest available
dependency versions. It will

* create a virtual environment,
* install your local package into the environment,
* upgrade specified dependency package(s), and
* run your test command.

Table Of Contents
-----------------

- [Install](#install)
- [Getting Started](#getting-started)
- [Options](#options)
- [Examples](#examples)
- [Contributing](#contributing)

Install
-------

Create a ``conda`` environment with Python 3.7+ and install from PyPI:

```console
$ python -m pip install edgetest
```

Getting Started
---------------

``edgetest`` allows multi-package, bleeding edge dependency testing. Suppose you have a package, ``mypackage``, with the following ``requirements.txt``:

```
pandas>=0.25.1,<=1.0.0
...
```

``edgetest`` allows you to test your package against the latest version of ``pandas``. If you run

```console
$ edgetest
```

the package will

1. Create a virtual environment in the ``.edgetest`` folder,
2. Install the local ``mypackage``: ``.edgetest/pandas/bin/python -m pip install .``,
3. Upgrade ``pandas``: ``.edgetest/pandas/bin/python -m pip install pandas --upgrade``,
4. Run ``.edgetest/pandas/bin/python -m pytest``, and
5. Repeat steps 1-4 for all packages in ``requirements.txt``.

After you run the command, you should get console output similar to the following:

```
============= =============== =================== =================
 Environment   Passing tests   Upgraded packages   Package version
------------- --------------- ------------------- -----------------
 pandas        True            pandas              1.2.4
============= =============== =================== =================
```

Options
-------

See the [advanced usage](https://capitalone.github.io/edgetest/usage.html) page.

Contributing
------------

See our [developer documentation](https://capitalone.github.io/edgetest/developer.html).

Roadmap
-------

Roadmap details can be found [here](https://capitalone.github.io/edgetest/roadmap.html).
