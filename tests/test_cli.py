from __future__ import annotations

import typing as t

import pytest

from pboot_pbatis import Pbatis
from pboot_pbatis.cli import add_models_to_shell


@pytest.mark.usefixtures("app_ctx")
def test_shell_context(db: Pbatis, Todo: t.Any) -> None:
    context = add_models_to_shell()
    assert context["db"] is db
    assert context["Todo"] is Todo
