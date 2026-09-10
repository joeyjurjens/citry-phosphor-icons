import re

import pytest
from citry import Citry

import citry_phosphor_icons
from citry_phosphor_icons import PhosphorIcons


def engine(**defaults):
    app = Citry(
        autodiscover=False,
        extensions=[PhosphorIcons],
        extensions_defaults={"phosphor": defaults} if defaults else None,
    )
    app.register_library(citry_phosphor_icons)
    return app


def paths(app, source):
    """The <path> data, which is what the weight and style actually select."""
    return re.findall(r'<path[^>]*d="([^"]+)"', app.render_template(source).serialize())


def test_the_engine_supplies_the_default_weight():
    app = engine(default_weight="bold")
    assert paths(app, '<c-icon name="house" />') == paths(
        app, '<c-icon name="house" weight="bold" />'
    )


def test_a_keyword_argument_beats_the_engine_default():
    app = engine(default_weight="bold")
    assert paths(app, '<c-icon name="house" weight="thin" />') != paths(
        app, '<c-icon name="house" />'
    )


def test_each_engine_keeps_its_own_defaults():
    source = '<c-icon name="house" />'
    assert paths(engine(default_weight="bold"), source) != paths(engine(), source)


def test_an_unknown_setting_is_rejected():
    with pytest.raises(Exception, match="unknown config field"):
        engine(default_wieght="bold")


def test_an_invalid_value_is_rejected():
    with pytest.raises(Exception, match="default_weight must be one of"):
        engine(default_weight="chunky")


def test_the_library_requires_its_extension():
    app = Citry(autodiscover=False)
    with pytest.raises(Exception, match="phosphor"):
        app.register_library(citry_phosphor_icons)


def named(tag):
    app = Citry(autodiscover=False, extensions=[PhosphorIcons])
    app.register_library(citry_phosphor_icons.library(tag))
    return app


def test_the_default_tag_is_c_icon():
    app = Citry(autodiscover=False, extensions=[PhosphorIcons])
    app.register_library(citry_phosphor_icons)
    assert "<svg" in app.render_template('<c-icon name="house" />').serialize()


def test_the_tag_can_be_chosen():
    app = named("whateveriwant-icon")
    assert "<svg" in app.render_template('<c-whateveriwant-icon name="house" />').serialize()


def test_choosing_a_tag_replaces_the_default_rather_than_adding_to_it():
    app = named("ph-icon")
    assert [n for n in app.components if "icon" in n] == ["ph-icon"]


def test_the_default_name_returns_the_shipped_manifest():
    assert citry_phosphor_icons.library() is citry_phosphor_icons.__citry_library__


def rendered_twice(lib, monkeypatch):
    """How often the component did its work, which is what caching skips."""
    from citry_phosphor_icons.components import icon as module

    calls = []
    real = module.get_svg_inner

    def counting(*args, **kwargs):
        calls.append(1)
        return real(*args, **kwargs)

    monkeypatch.setattr(module, "get_svg_inner", counting)
    app = Citry(autodiscover=False, extensions=[PhosphorIcons])
    cls = app.register_library(lib).component(lib.components[0])
    for _ in range(2):
        app.render_template(f'<c-{cls.name or "icon"} name="house" />')
    return len(calls)


def test_rendering_is_cached_by_default(monkeypatch):
    assert rendered_twice(citry_phosphor_icons.library(), monkeypatch) == 1


def test_caching_can_be_turned_off(monkeypatch):
    assert rendered_twice(citry_phosphor_icons.library(cache=False), monkeypatch) == 2
