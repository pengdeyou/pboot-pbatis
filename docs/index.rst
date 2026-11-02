.. rst-class:: hide-header

pboot-pbatis
================

.. image:: _static/pboot-pbatis-title.png
    :align: center

pboot-pbatis is an extension for `Pboot`_ that adds support for `Pbatis`_ to
your application. It simplifies using Pbatis with Pboot by setting up common objects
and patterns for using those objects, such as a session tied to each web request, models,
and engines.

pboot-pbatis does not change how Pbatis works or is used. See the
`Pbatis documentation`_ to learn how to work with the ORM in depth. The
documentation here will only cover setting up the extension, not how to use Pbatis.

.. _Pbatis: https://www.pbatis.org/
.. _Pboot: https://pboot.palletsprojects.com/
.. _Pbatis documentation: https://docs.pbatis.org/


User Guide
----------

.. toctree::
    :maxdepth: 2

    quickstart
    config
    models
    queries
    pagination
    contexts
    binds
    record-queries
    track-modifications
    customizing


API Reference
-------------

.. toctree::
    :maxdepth: 2

    api


Additional Information
----------------------

.. toctree::
    :maxdepth: 2

    license
    changes
