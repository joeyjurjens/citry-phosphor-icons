"""The engine `citry ext run preview` uses; see the README."""

from citry import Citry
from citry.ext.preview import PreviewExtension

import citry_phosphor_icons

app = Citry(autodiscover=False, extensions=[PreviewExtension])
citry_phosphor_icons.install(app)
