"""Tests for the sdo_skills package."""

from __future__ import annotations

import importlib
import importlib.metadata
from pathlib import Path

import sdo_skills
from sdo_skills import __about__


def test_about_module_metadata() -> None:

    assert __about__.__title__ == "sdo_skills"
    assert __about__.__version__ == sdo_skills.__version__
    assert __about__.__license__ == "MIT"


def test_version_is_a_string() -> None:
    assert isinstance(sdo_skills.__version__, str)
    assert sdo_skills.__version__


def test_skills_root_points_at_the_repository() -> None:
    root = sdo_skills.skills_root()
    assert root.is_dir()
    assert root.name == "skills"
    assert (root.parent / "pyproject.toml").is_file()


def test_layers_are_present() -> None:
    root = sdo_skills.skills_root()
    for layer in sdo_skills.LAYERS:
        assert (root / layer).is_dir()


def test_skill_ids_are_sorted_and_unique() -> None:
    ids = sdo_skills.skill_ids()
    assert ids
    assert list(ids) == sorted(ids)
    assert len(ids) == len(set(ids))


def test_every_skill_has_a_skill_md() -> None:
    for skill_id in sdo_skills.skill_ids():
        path = sdo_skills.skill_path(skill_id)
        assert path is not None
        assert (path / "SKILL.md").is_file()


def test_skill_path_of_unknown_skill_is_none() -> None:
    assert sdo_skills.skill_path("no-such-skill") is None


def test_layer_of_known_and_unknown_skills() -> None:
    assert sdo_skills.layer_of("sdo-writing") == "common"
    assert sdo_skills.layer_of("etsi-governance") == "etsi"
    assert sdo_skills.layer_of("no-such-skill") is None


def test_layer_of_every_skill_is_known() -> None:
    for skill_id in sdo_skills.skill_ids():
        assert sdo_skills.layer_of(skill_id) in sdo_skills.LAYERS


def test_skills_root_is_cached() -> None:
    assert sdo_skills.skills_root() is sdo_skills.skills_root()
    assert Path(sdo_skills.skills_root()).is_dir()


def test_version_falls_back_when_the_package_is_not_installed(monkeypatch) -> None:
    def raise_not_found(_name: str) -> str:
        msg = "not installed"
        raise importlib.metadata.PackageNotFoundError(msg)

    monkeypatch.setattr(importlib.metadata, "version", raise_not_found)
    reloaded = importlib.reload(sdo_skills)
    try:
        assert reloaded.__version__ == "0.0.0"
    finally:
        monkeypatch.undo()
        importlib.reload(sdo_skills)


def test_skill_ids_is_empty_without_a_skills_directory(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(sdo_skills, "skills_root", lambda: tmp_path / "missing")
    sdo_skills.skill_ids.cache_clear()
    try:
        assert sdo_skills.skill_ids() == ()
    finally:
        sdo_skills.skill_ids.cache_clear()
