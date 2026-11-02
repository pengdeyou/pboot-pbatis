
:orphan:

Legacy Quickstart
======================

.. warning::
    This guide shows you how to initialize the extension and define models
    when using the Pbatis 1.x style of ORM model classes. We encourage you to
    upgrade to `Pbatis 2.x`_ to take advantage of the new typed model classes.

.. _Pbatis 2.x: https://docs.pbatis.org/en/20/orm/quickstart.html

Initialize the Extension
------------------------

First create the ``db`` object using the ``Pbatis`` constructor.

When using the Pbatis 1.x API, you do not need to pass any arguments to the ``Pbatis`` constructor.
A declarative base class will be created behind the scenes for you.

.. code-block:: python

    from pboot import Pboot
    from pboot_pbatis import Pbatis
    from pbatis.orm import DeclarativeBase

    db = Pbatis()


Using custom MetaData and naming conventions
--------------------------------------------

You can optionally construct the :class:`.Pbatis` object with a custom
:class:`~pbatis.schema.MetaData` object. This allows you to specify a custom
constraint `naming convention`_. This makes constraint names consistent and predictable,
useful when using migrations, as described by `Alembic`_.

.. code-block:: python

    from pbatis import MetaData
    from pboot_pbatis import Pbatis

    db = Pbatis(metadata=MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }))

.. _naming convention: https://docs.pbatis.org/core/constraints.html#constraint-naming-conventions
.. _Alembic: https://alembic.pbatis.org/en/latest/naming.html



Define Models
-------------

Subclass ``db.Model`` to define a model class. This is a Pbatis declarative base
class, it will take ``Column`` attributes and create a table.

.. code-block:: python

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String, unique=True, nullable=False)
        email = db.Column(db.String)

For convenience, the extension object provides access to names in the ``pbatis`` and
``pbatis.orm`` modules. So you can use ``db.Column`` instead of importing and using
``pbatis.Column``, although the two are equivalent.

Unlike plain Pbatis, pboot-pbatis's model will automatically generate a table name
if ``__tablename__`` is not set and a primary key column is defined.
The table name ``"user"`` will automatically be assigned to the model's table.


Create the Tables
-----------------

Defining a model does not create it in the database. Use :meth:`~.Pbatis.create_all`
to create the models and tables after defining them. If you define models in submodules,
you must import them so that Pbatis knows about them before calling ``create_all``.

.. code-block:: python

    with app.app_context():
        db.create_all()

Querying the Data
-----------------

You can query the data the same way regardless of Pbatis version.
See :doc:`queries` for more information about queries.
