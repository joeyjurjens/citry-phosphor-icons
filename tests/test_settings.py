import re

import pytest
from citry import Citry, merge_attrs

import citry_phosphor_icons
from citry_phosphor_icons import Icon


def engine(**kwargs):
    app = Citry(autodiscover=False)
    citry_phosphor_icons.install(app, **kwargs)
    return app


def paths(app, source):
    """The <path> data, which is what the weight and style actually select."""
    return re.findall(r'<path[^>]*d="([^"]+)"', app.render_template(source).serialize())


def test_the_library_supplies_a_default_weight():
    app = engine(weight="bold")
    assert paths(app, '<c-icon name="house" />') == paths(
        app, '<c-icon name="house" weight="bold" />'
    )


def test_a_keyword_argument_beats_the_default():
    app = engine(weight="bold")
    assert paths(app, '<c-icon name="house" weight="thin" />') != paths(
        app, '<c-icon name="house" />'
    )


def test_each_engine_keeps_its_own_defaults():
    source = '<c-icon name="house" />'
    assert paths(engine(weight="bold"), source) != paths(engine(), source)


def test_an_invalid_value_is_rejected():
    with pytest.raises(ValueError, match="weight must be one of"):
        engine(weight="chunky")


def test_the_tag_can_be_chosen():
    assert [n for n in engine(name="ph-icon").components if "icon" in n] == ["ph-icon"]


def test_your_own_subclass_can_be_published():
    class MyIcon(Icon):
        def get_attrs(self, kwargs):
            return merge_attrs({"class": "icon"}, super().get_attrs(kwargs))

    app = engine(override=MyIcon)
    assert 'class="icon"' in app.render_template('<c-icon name="house" />').serialize()


def test_the_default_install_reuses_the_shipped_manifest():
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
    app = Citry(autodiscover=False)
    app.register_library(lib)
    for _ in range(2):
        app.render_template('<c-icon name="house" />')
    return len(calls)


def test_rendering_is_cached_by_default(monkeypatch):
    assert rendered_twice(citry_phosphor_icons.library(), monkeypatch) == 1


def test_caching_can_be_turned_off(monkeypatch):
    assert rendered_twice(citry_phosphor_icons.library(cache=False), monkeypatch) == 2
