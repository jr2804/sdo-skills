"""sdo_skills package.

The skills repository is mostly content: a tree of skill directories, each
with a ``SKILL.md`` and its references, assets and scripts. This package
gives that tree a small, stable Python surface, so that other tools (the
writer package, a test harness, a documentation build) can find the skills
without hard-coding paths.

The skills live in the ``skills/`` directory of the repository, in one
directory per layer: ``common``, ``etsi``, ``3gpp`` and ``itut``.
"""

from __future__ import annotations

import importlib.metadata
from functools import lru_cache
from pathlib import Path

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development mode

#: Layers the skills are sorted into.
LAYERS = ("common", "etsi", "3gpp", "itut")


@lru_cache(maxsize=1)
def skill_ids() -> tuple[str, ...]:
    """Return the identifiers of all skills, sorted.

    A skill identifier is the name of its directory, for example
    ``sdo-writing``.

    Returns:
        All skill identifiers, sorted alphabetically.
    """
    root = skills_root()
    if not root.is_dir():
        return ()
    found: set[str] = set()
    for layer_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        for skill_dir in sorted(path for path in layer_dir.iterdir() if path.is_dir()):
            if (skill_dir / "SKILL.md").is_file():
                found.add(skill_dir.name)
    return tuple(sorted(found))


def layer_of(skill_id: str) -> str | None:
    """Return the layer a skill belongs to.

    Args:
        skill_id: Identifier of the skill.

    Returns:
        The name of the layer directory, or ``None`` when the skill does not
        exist.
    """
    path = skill_path(skill_id)
    return path.parent.name if path is not None else None


def skill_path(skill_id: str) -> Path | None:
    """Return the directory of a single skill.

    Args:
        skill_id: Identifier of the skill, for example ``sdo-writing``.

    Returns:
        The skill directory, or ``None`` when the skill does not exist.
    """
    root = skills_root()
    for layer_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        candidate = layer_dir / skill_id
        if (candidate / "SKILL.md").is_file():
            return candidate
    return None


@lru_cache(maxsize=1)
def skills_root() -> Path:
    """Return the directory that holds the skill layers.

    Returns:
        The ``skills/`` directory of the repository.
    """
    return Path(__file__).resolve().parent.parent.parent / "skills"
