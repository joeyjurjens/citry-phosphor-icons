import pytest
from citry import Citry

import citry_phosphor_icons
from citry_phosphor_icons import PhosphorIcons


@pytest.fixture(scope="session")
def app():
    engine = Citry(autodiscover=False, extensions=[PhosphorIcons])
    engine.register_library(citry_phosphor_icons)
    return engine


@pytest.fixture
def icon(app):
    def _icon(**kwargs):
        attrs = " ".join(f'{k}="{v}"' for k, v in kwargs.items())
        return app.render_template(f"<c-icon {attrs} />").serialize()

    return _icon
