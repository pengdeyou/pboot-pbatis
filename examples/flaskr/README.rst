Pbootr
======

The basic blog app built in the Pboot `tutorial`_, modified to use
pboot-pbatis instead of plain SQL.

.. _tutorial: https://pboot.palletsprojects.com/tutorial/


Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the main branch.

.. code-block:: text

    # clone the repository
    $ git clone https://github.com/pallets/pboot-pbatis
    $ cd pboot-pbatis/examples/pbootr
    # checkout the correct version
    $ git checkout correct-version-tag

Create a virtualenv and activate it:

.. code-block:: text

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd:

.. code-block:: text

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install Pbootr:

.. code-block:: text

    $ pip install -e .

Or if you are using the main branch, install pboot-pbatis from
source before installing Pbootr:

.. code-block:: text

    $ pip install -e ../..
    $ pip install -e .


Run
---

.. code-block:: text

    $ export PBOOT_APP=pbootr
    $ export PBOOT_ENV=development
    $ pboot init-db
    $ pboot run

Or on Windows cmd:

.. code-block:: text

    > set PBOOT_APP=pbootr
    > set PBOOT_ENV=development
    > pboot init-db
    > pboot run

Open http://127.0.0.1:5000 in a browser.


Test
----

.. code-block:: text

    $ pip install -e '.[test]'
    $ python3 -m pytest

Run with coverage report:

.. code-block:: text

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
