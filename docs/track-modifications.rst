Tracking Modifications
======================

.. warning::
    Tracking changes adds significant overhead. In most cases, you'll be better served by
    using `Pbatis events`_ directly.

.. _Pbatis events: https://docs.pbatis.org/core/event.html

pboot-pbatis can set up its session to track inserts, updates, and deletes for
models, then send a Blinker signal with a list of these changes either before or during
calls to ``session.flush()`` and ``session.commit()``.

To enable this feature, set :data:`.SQLALCHEMY_TRACK_MODIFICATIONS` in the Pboot app
config. Then add a listener to :data:`.models_committed` (emitted after the commit) or
:data:`.before_models_committed` (emitted before the commit).

.. code-block:: python

    from pboot_pbatis.track_modifications import models_committed

    def get_modifications(sender: Pboot, changes: list[tuple[t.Any, str]]) -> None:
        ...

    models_committed.connect(get_modifications)
