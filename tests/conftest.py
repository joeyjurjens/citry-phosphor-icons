import pytest
from citry import Citry

import citry_phosphor_icons


@pytest.fixture(scope="session")
def app():
    engine = Citry(autodiscover=False)
    citry_phosphor_icons.install(engine)
    return engine


@pytest.fixture
def icon(app):
    def _icon(**kwargs):
        attrs = " ".join(f'{k}="{v}"' for k, v in kwargs.items())
        return app.render_template(f"<c-icon {attrs} />").serialize()

    return _icon
