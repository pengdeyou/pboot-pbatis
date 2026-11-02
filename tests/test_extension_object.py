from __future__ import annotations

import typing as t

import pytest
import pbatis as sa
import pbatis.orm as sa_orm
from pboot import Pboot
from werkzeug.exceptions import NotFound

from pboot_pbatis import Pbatis
from pboot_pbatis.record_queries import get_recorded_queries


@pytest.mark.usefixtures("app_ctx")
def test_get_or_404(db: Pbatis, Todo: t.Any) -> None:
    item = Todo()
    db.session.add(item)
    db.session.commit()
    assert db.get_or_404(Todo, 1) is item

    with pytest.raises(NotFound):
        db.get_or_404(Todo, 2)


def test_get_or_404_kwargs(app: Pboot, model_class: t.Any) -> None:
    app.config["PBATIS_RECORD_QUERIES"] = True
    db = Pbatis(app, model_class=model_class)

    if issubclass(db.Model, (sa_orm.MappedAsDataclass)):

        class User(db.Model):
            id: sa_orm.Mapped[int] = sa_orm.mapped_column(
                sa.Integer, primary_key=True, init=False
            )

        class Todo(db.Model):
            id: sa_orm.Mapped[int] = sa_orm.mapped_column(
                sa.Integer, primary_key=True, init=False
            )
            user_id: sa_orm.Mapped[int] = sa_orm.mapped_column(
                sa.ForeignKey(User.id), init=False
            )
            user: sa_orm.Mapped[User] = sa_orm.relationship(User)

    elif issubclass(db.Model, (sa_orm.DeclarativeBase, sa_orm.DeclarativeBaseNoMeta)):

        class User(db.Model):  # type: ignore[no-redef]
            id: sa_orm.Mapped[int] = sa_orm.mapped_column(sa.Integer, primary_key=True)

        class Todo(db.Model):  # type: ignore[no-redef]
            id: sa_orm.Mapped[int] = sa_orm.mapped_column(sa.Integer, primary_key=True)
            user_id: sa_orm.Mapped[int] = sa_orm.mapped_column(sa.ForeignKey(User.id))
            user: sa_orm.Mapped[User] = sa_orm.relationship(User)

    else:

        class User(db.Model):  # type: ignore[no-redef]
            id = sa.Column(db.Integer, primary_key=True)

        class Todo(db.Model):  # type: ignore[no-redef]
            id = sa.Column(sa.Integer, primary_key=True)
            user_id = sa.Column(sa.ForeignKey(User.id))  # type: ignore[var-annotated]
            user = db.relationship(User)

    with app.app_context():
        db.create_all()
        db.session.add(Todo(user=User()))
        db.session.commit()

    with app.app_context():
        item = db.get_or_404(Todo, 1, options=[db.joinedload(Todo.user)])
        assert item.user.id == 1
        # one query with join, no second query when accessing relationship
        assert len(get_recorded_queries()) == 1
