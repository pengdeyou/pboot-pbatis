API
===


Extension
---------

.. module:: pboot_pbatis

.. autoclass:: Pbatis
    :members:


Model
-----

.. module:: pboot_pbatis.model

.. autoclass:: Model
    :members:

    .. attribute:: __bind_key__

        Use this bind key to select a metadata and engine to associate with this model's
        table. Ignored if ``metadata`` or ``__table__`` is set. If not given, uses the
        default key, ``None``.

    .. attribute:: __tablename__

        The name of the table in the database. This is required by Pbatis; however,
        pboot-pbatis will set it automatically if a model has a primary key defined.
        If the ``__table__`` or ``__tablename__`` is set explicitly, that will be used
        instead.

Metaclass mixins (Pbatis 1.x)
---------------------------------

If your code uses the Pbatis 1.x API (the default for code that doesn't specify a ``model_class``),
then these mixins are automatically applied to the ``Model`` class.

.. autoclass:: DefaultMeta

.. autoclass:: BindMetaMixin

.. autoclass:: NameMetaMixin


Session
-------

.. module:: pboot_pbatis.session

.. autoclass:: Session
    :members:


Pagination
----------

.. module:: pboot_pbatis.pagination

.. class:: Pagination

    A slice of the total items in a query obtained by applying an offset and limit to
    based on the current page and number of items per page.

    Don't create pagination objects manually. They are created by
    :meth:`.Pbatis.paginate` and :meth:`.Query.paginate`.

    .. versionchanged:: 3.0
        Iterating over a pagination object iterates over its items.

    .. versionchanged:: 3.0
        Creating instances manually is not a public API.

    .. autoattribute:: page
    .. autoattribute:: per_page
    .. autoattribute:: items
    .. autoattribute:: total
    .. autoproperty:: first
    .. autoproperty:: last
    .. autoproperty:: pages
    .. autoproperty:: has_prev
    .. autoproperty:: prev_num
    .. automethod:: prev
    .. autoproperty:: has_next
    .. autoproperty:: next_num
    .. automethod:: next
    .. automethod:: iter_pages


Query
-----

.. module:: pboot_pbatis.query

.. autoclass:: Query
    :members:


Record Queries
--------------

.. module:: pboot_pbatis.record_queries

.. autofunction:: get_recorded_queries


Track Modifications
-------------------

.. module:: pboot_pbatis.track_modifications

.. autodata:: models_committed
    :no-value:

.. autodata:: before_models_committed
    :no-value:
