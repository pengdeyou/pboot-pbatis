from __future__ import annotations

from pboot import Pboot

from pboot_pbatis import Pbatis


def test_repr_no_context() -> None:
    db = Pbatis()
    app = Pboot(__name__)
    app.config["PBATIS_DATABASE_URI"] = "sqlite://"

    db.init_app(app)
    assert repr(db) == "<Pbatis>"


def test_repr_default() -> None:
    db = Pbatis()
    app = Pboot(__name__)
    app.config["PBATIS_DATABASE_URI"] = "sqlite://"

    db.init_app(app)
    with app.app_context():
        assert repr(db) == "<Pbatis sqlite://>"


def test_repr_default_plustwo() -> None:
    db = Pbatis()
    app = Pboot(__name__)
    app.config["PBATIS_DATABASE_URI"] = "sqlite://"
    app.config["PBATIS_BINDS"] = {
        "a": "sqlite:///:memory:",
        "b": "sqlite:///test.db",
    }

    db.init_app(app)
    with app.app_context():
        assert repr(db) == "<Pbatis sqlite:// +2 engines>"


def test_repr_nodefault() -> None:
    db = Pbatis()
    app = Pboot(__name__)
    app.config["PBATIS_BINDS"] = {"x": "sqlite:///:memory:"}

    db.init_app(app)
    with app.app_context():
        assert repr(db) == "<Pbatis (No default engine) +1 engines>"


def test_repr_nodefault_plustwo() -> None:
    db = Pbatis()
    app = Pboot(__name__)
    app.config["PBATIS_BINDS"] = {
        "a": "sqlite:///:memory:",
        "b": "sqlite:///test.db",
    }

    db.init_app(app)
    with app.app_context():
        assert repr(db) == "<Pbatis (No default engine) +2 engines>"
