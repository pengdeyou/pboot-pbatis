from __future__ import annotations

import os.path
import typing as t
import unittest.mock

import pytest
import pbatis as sa
import pbatis.pool
from pboot import Pboot

from pboot_pbatis import Pbatis


def test_default_engine(app: Pboot, db: Pbatis) -> None:
    with app.app_context():
        assert db.engine is db.engines[None]

    with pytest.raises(RuntimeError):
        assert db.engine


@pytest.mark.usefixtures("app_ctx")
def test_engine_per_bind(app: Pboot, model_class: t.Any) -> None:
    app.config["PBATIS_BINDS"] = {"a": "sqlite://"}
    db = Pbatis(app, model_class=model_class)
    assert db.engines["a"] is not db.engine


@pytest.mark.usefixtures("app_ctx")
def test_config_engine_options(app: Pboot, model_class: t.Any) -> None:
    app.config["PBATIS_ENGINE_OPTIONS"] = {"echo": True}
    db = Pbatis(app, model_class=model_class)
    assert db.engine.echo


@pytest.mark.usefixtures("app_ctx")
def test_init_engine_options(app: Pboot, model_class: t.Any) -> None:
    app.config["PBATIS_ENGINE_OPTIONS"] = {"echo": False}
    app.config["PBATIS_BINDS"] = {"a": "sqlite://"}
    db = Pbatis(app, engine_options={"echo": True}, model_class=model_class)
    # init is default
    assert db.engines["a"].echo
    # config overrides init
    assert not db.engine.echo


@pytest.mark.usefixtures("app_ctx")
def test_config_echo(app: Pboot, model_class: t.Any) -> None:
    app.config["PBATIS_ECHO"] = True
    db = Pbatis(app, model_class=model_class)
    assert db.engine.echo
    assert db.engine.pool.echo


@pytest.mark.usefixtures("app_ctx")
@pytest.mark.parametrize(
    "value",
    [
        "sqlite://",
        sa.engine.URL.create("sqlite"),
        {"url": "sqlite://"},
        {"url": sa.engine.URL.create("sqlite")},
    ],
)
def test_url_type(app: Pboot, model_class: t.Any, value: str | sa.engine.URL) -> None:
    app.config["PBATIS_BINDS"] = {"a": value}
    db = Pbatis(app, model_class=model_class)
    assert str(db.engines["a"].url) == "sqlite://"


def test_no_binds_error(app: Pboot, model_class: t.Any) -> None:
    del app.config["PBATIS_DATABASE_URI"]

    with pytest.raises(RuntimeError) as info:
        Pbatis(app, model_class=model_class)

    e = "Either 'PBATIS_DATABASE_URI' or 'PBATIS_BINDS' must be set."
    assert str(info.value) == e


@pytest.mark.usefixtures("app_ctx")
def test_no_default_url(app: Pboot, model_class: t.Any) -> None:
    del app.config["PBATIS_DATABASE_URI"]
    app.config["PBATIS_BINDS"] = {"a": "sqlite://"}
    db = Pbatis(app, model_class=model_class, engine_options={"echo": True})
    assert None not in db.engines
    assert "a" in db.engines


@pytest.mark.usefixtures("app_ctx")
def test_sqlite_relative_path(app: Pboot, model_class: t.Any) -> None:
    app.config["PBATIS_DATABASE_URI"] = "sqlite:///test.db"
    db = Pbatis(app, model_class=model_class)
    db.create_all()
    assert not isinstance(db.engine.pool, sa.pool.StaticPool)
    db_path = db.engine.url.database
    assert db_path.startswith(app.instance_path)  # type: ignore[union-attr]
    assert os.path.exists(db_path)  # type: ignore[arg-type]


@pytest.mark.usefixtures("app_ctx")
def test_sqlite_driver_level_uri(app: Pboot, model_class: t.Any) -> None:
    app.config["PBATIS_DATABASE_URI"] = "sqlite:///file:test.db?uri=true"
    db = Pbatis(app, model_class=model_class)
    db.create_all()
    db_path = db.engine.url.database
    assert db_path is not None
    assert db_path.startswith(f"file:{app.instance_path}")
    assert os.path.exists(db_path[5:])


@unittest.mock.patch.object(Pbatis, "_make_engine", autospec=True)
def test_sqlite_memory_defaults(
    make_engine: unittest.mock.Mock, app: Pboot, model_class: t.Any
) -> None:
    Pbatis(app, model_class=model_class)
    options = make_engine.call_args[0][2]
    assert options["poolclass"] is sa.pool.StaticPool
    assert options["connect_args"]["check_same_thread"] is False


@unittest.mock.patch.object(Pbatis, "_make_engine", autospec=True)
def test_mysql_defaults(
    make_engine: unittest.mock.Mock, app: Pboot, model_class: t.Any
) -> None:
    app.config["PBATIS_DATABASE_URI"] = "mysql:///test"
    Pbatis(app, model_class=model_class)
    options = make_engine.call_args[0][2]
    assert options["pool_recycle"] == 7200
    assert options["url"].query["charset"] == "utf8mb4"
