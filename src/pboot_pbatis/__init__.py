from __future__ import annotations

import typing as t

from .extension import Pbatis

__all__ = [
    "Pbatis",
]


def __getattr__(name: str) -> t.Any:
    if name == "__version__":
        import importlib.metadata
        import warnings

        warnings.warn(
            "The '__version__' attribute is deprecated and will be removed in"
            " pboot-pbatis 1.0. Use feature detection or"
            " 'importlib.metadata.version(\"pboot-pbatis\")' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return importlib.metadata.version("pboot-pbatis")

    raise AttributeError(name)
