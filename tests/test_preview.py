import pytest
from citry import Citry
from citry.ext.preview import PreviewExtension

import citry_phosphor_icons
from citry_phosphor_icons import Icon
from citry_phosphor_icons.preview import SAMPLE


@pytest.fixture(scope="session")
def variants():
    return Icon.Preview().variants()


def test_every_weight_and_style_is_shown(variants):
    from py_phosphor_icons import VALID_STYLES, VALID_WEIGHTS

    slugs = {v.slug for v in variants}
    assert {f"{s}-{w}" for s in VALID_STYLES for w in VALID_WEIGHTS} <= slugs


def test_the_presentation_arguments_are_shown(variants):
    slugs = {v.slug for v in variants}
    assert {"sized", "colored", "mirrored", "extra-attributes"} <= slugs


def test_slugs_are_unique(variants):
    slugs = [v.slug for v in variants]
    assert len(slugs) == len(set(slugs))


def test_every_variant_renders():
    """Params are the component's own kwargs, so each one has to be valid."""
    app = Citry(autodiscover=False, extensions=[PreviewExtension])
    installed = citry_phosphor_icons.install(app)
    component = installed.component(Icon)
    for spec in Icon.Preview().variants():
        assert "<svg" in str(component(**dict(spec.params)).render())


def test_previews_do_not_require_the_extension():
    """A library must install into an engine that has no preview extension."""
    app = Citry(autodiscover=False)
    citry_phosphor_icons.install(app)
    assert "<svg" in app.render_template(f'<c-icon name="{SAMPLE}" />').serialize()
