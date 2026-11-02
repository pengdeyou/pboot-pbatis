from __future__ import annotations

import os

import pytest
import pbatis as sa
import pbatis.orm as sa_orm
from pboot import Pboot

from pboot_pbatis import Pbatis
from pboot_pbatis.record_queries import get_recorded_queries


@pytest.mark.usefixtures("app_ctx")
def test_query_info(app: Pboot) -> None:
    app.config["PBATIS_RECORD_QUERIES"] = True
    db = Pbatis(app)

    # Copied and pasted from conftest.py
    if issubclass(db.Model, (sa_orm.MappedAsDataclass)):

        class Todo(db.Model):
            id: sa_orm.Mapped[int] = sa_orm.mapped_column(
                sa.Integer, init=False, primary_key=True
            )
            title: sa_orm.Mapped[str] = sa_orm.mapped_column(
                sa.String, nullable=True, default=None
            )

    elif issubclass(db.Model, (sa_orm.DeclarativeBase, sa_orm.DeclarativeBaseNoMeta)):

        class Todo(db.Model):  # type: ignore[no-redef]
            id: sa_orm.Mapped[int] = sa_orm.mapped_column(sa.Integer, primary_key=True)
            title: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String, nullable=True)

    else:

        class Todo(db.Model):  # type: ignore[no-redef]
            id = sa.Column(sa.Integer, primary_key=True)
            title = sa.Column(sa.String)

    db.create_all()
    db.session.execute(sa.select(Todo).filter(Todo.id < 5)).scalars()
    info = get_recorded_queries()[-1]
    assert info.statement is not None
    assert "SELECT" in info.statement
    assert "FROM todo" in info.statement
    assert info.parameters[0][0] == 5
    assert info.duration == info.end_time - info.start_time
    assert os.path.join("tests", "test_record_queries.py:") in info.location
    assert "(test_query_info)" in info.location
