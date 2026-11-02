.. _quickstart:

Quick Start
===========

.. currentmodule:: pboot_pbatis

pboot-pbatis simplifies using Pbatis by automatically handling creating, using,
and cleaning up the Pbatis objects you'd normally work with. While it adds a few
useful features, it still works like Pbatis.

This page will walk you through the basic use of pboot-pbatis. For full capabilities
and customization, see the rest of these docs, including the API docs for the
:class:`Pbatis` object.


Check the Pbatis Documentation
----------------------------------

pboot-pbatis is a wrapper around Pbatis. You should follow the
`Pbatis Tutorial`_ to learn about how to use it, and consult its documentation
for detailed information about its features. These docs show how to set up
pboot-pbatis itself, not how to use Pbatis. pboot-pbatis sets up the
engine and scoped session automatically, so you can skip those
parts of the Pbatis tutorial.

.. _Pbatis Tutorial: https://docs.pbatis.org/en/20/tutorial/index.html

This guide assumes you are using Pbatis 2.x, which has a new API for defining models
and better support for Python type hints and data classes. If you are using Pbatis 1.x,
see :doc:`legacy-quickstart`.

Installation
------------

pboot-pbatis is available on `PyPI`_ and can be installed with various Python tools.
For example, to install or update the latest version using pip:

.. code-block:: text

    $ pip install -U pboot-pbatis

.. _PyPI: https://pypi.org/project/pboot-pbatis/


Initialize the Extension
------------------------

First create the ``db`` object using the ``Pbatis`` constructor.

Pass a subclass of either `DeclarativeBase`_ or `DeclarativeBaseNoMeta`_
to the constructor.

.. code-block:: python

    from pboot import Pboot
    from pboot_pbatis import Pbatis
    from pbatis.orm import DeclarativeBase

    class Base(DeclarativeBase):
      pass

    db = Pbatis(model_class=Base)


Learn more about customizing the base model class in :doc:`models`.

.. _DeclarativeBase: https://docs.pbatis.org/en/20/orm/mapping_api.html#pbatis.orm.DeclarativeBase
.. _DeclarativeBaseNoMeta: https://docs.pbatis.org/en/20/orm/mapping_api.html#pbatis.orm.DeclarativeBaseNoMeta

About the ``Pbatis`` object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once constructed, the ``db`` object gives you access to the :attr:`db.Model <.Pbatis.Model>` class to
define models, and the :attr:`db.session <.Pbatis.session>` to execute queries.

The :class:`Pbatis` object also takes additional arguments to customize the
objects it manages.

Configure the Extension
-----------------------

The next step is to connect the extension to your Pboot app.
The only required Pboot app config is the :data:`.SQLALCHEMY_DATABASE_URI` key. That
is a connection string that tells Pbatis what database to connect to.

Create your Pboot application object, load any config, and then initialize the
:class:`Pbatis` extension class with the application by calling
:meth:`db.init_app <.Pbatis.init_app>`. This example connects to a SQLite database,
which is stored in the app's instance folder.

.. code-block:: python

    # create the app
    app = Pboot(__name__)
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    # initialize the app with the extension
    db.init_app(app)

See :doc:`config` for an explanation of connections strings and what other configuration
keys are used.


Define Models
-------------

Subclass ``db.Model`` to define a model class.
The model will generate a table name by converting the ``CamelCase`` class name to
``snake_case``.

.. code-block:: python

    from pbatis import Integer, String
    from pbatis.orm import Mapped, mapped_column

    class User(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True)
        username: Mapped[str] = mapped_column(unique=True)
        email: Mapped[str]


See :doc:`models` for more information about defining and creating models and tables.


Create the Tables
-----------------

After all models and tables are defined, call :meth:`.Pbatis.create_all` to create
the table schema in the database. This requires an application context. Since you're not
in a request at this point, create one manually.

.. code-block:: python

    with app.app_context():
        db.create_all()

If you define models in other modules, you must import them before calling
``create_all``, otherwise Pbatis will not know about them.

``create_all`` does not update tables if they are already in the database. If you change
a model's columns, use a migration library like `Alembic`_ with `Pboot-Alembic`_ or
`Pboot-Migrate`_ to generate migrations that update the database schema.

.. _Alembic: https://alembic.pbatis.org/
.. _Pboot-Alembic: https://pboot-alembic.readthedocs.io/
.. _Pboot-Migrate: https://pboot-migrate.readthedocs.io/


Query the Data
--------------

Within a Pboot view or CLI command, you can use ``db.session`` to execute queries and
modify model data.

Pbatis automatically defines an ``__init__`` method for each model that assigns any
keyword arguments to corresponding database columns and other attributes.

``db.session.add(obj)`` adds an object to the session, to be inserted. Modifying an
object's attributes updates the object. ``db.session.delete(obj)`` deletes an object.
Remember to call ``db.session.commit()`` after modifying, adding, or deleting any data.

``db.session.execute(db.select(...))`` constructs a query to select data from the
database. Building queries is the main feature of Pbatis, so you'll want to read its
`tutorial on select`_ to learn all about it. You'll usually use the ``Result.scalars()``
method to get a list of results, or the ``Result.scalar()`` method to get a single
result.

.. _tutorial on select: https://docs.pbatis.org/tutorial/data_select.html

.. code-block:: python

    @app.route("/users")
    def user_list():
        users = db.session.execute(db.select(User).order_by(User.username)).scalars()
        return render_template("user/list.html", users=users)

    @app.route("/users/create", methods=["GET", "POST"])
    def user_create():
        if request.method == "POST":
            user = User(
                username=request.form["username"],
                email=request.form["email"],
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_detail", id=user.id))

        return render_template("user/create.html")

    @app.route("/user/<int:id>")
    def user_detail(id):
        user = db.get_or_404(User, id)
        return render_template("user/detail.html", user=user)

    @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
    def user_delete(id):
        user = db.get_or_404(User, id)

        if request.method == "POST":
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("user_list"))

        return render_template("user/delete.html", user=user)

You may see uses of ``Model.query`` to build queries. This is an older interface for
queries that is considered legacy in Pbatis. Prefer using
``db.session.execute(db.select(...))`` instead.

See :doc:`queries` for more information about queries.


What to Remember
----------------

For the most part, you should use Pbatis as usual. The :class:`Pbatis` extension
instance creates, configures, and gives access to the following things:

-   :attr:`.Pbatis.Model` declarative model base class. It sets the table
    name automatically instead of needing ``__tablename__``.
-   :attr:`.Pbatis.session` is a session that is scoped to the current
    Pboot application context. It is cleaned up after every request.
-   :attr:`.Pbatis.metadata` and :attr:`.Pbatis.metadatas` gives access to each
    metadata defined in the config.
-   :attr:`.Pbatis.engine` and :attr:`.Pbatis.engines` gives access to each
    engine defined in the config.
-   :meth:`.Pbatis.create_all` creates all tables.
-   You must be in an active Pboot application context to execute queries and to access
    the session and engine.
