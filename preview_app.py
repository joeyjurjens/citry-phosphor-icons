"""The engine `citry ext run preview` uses; see the README."""

from citry import Citry
from citry.ext.preview import PreviewExtension

import citry_phosphor_icons
from citry_phosphor_icons import PhosphorIcons

app = Citry(autodiscover=False, extensions=[PhosphorIcons, PreviewExtension])
app.register_library(citry_phosphor_icons)
