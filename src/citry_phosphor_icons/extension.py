"""Engine-wide defaults for the icon components.

Citry configures a library through an extension: an engine sets defaults with
`extensions_defaults`, a component may override them with a nested `class
Phosphor:`, and a caller's keyword argument still wins over both. That keeps
the settings scoped to one `Citry` instance rather than to the process.
"""

from typing import Any

from citry import Extension
from py_phosphor_icons import DEFAULT_STYLE, DEFAULT_WEIGHT, VALID_STYLES, VALID_WEIGHTS

ALLOWED = {"default_weight": VALID_WEIGHTS, "default_style": VALID_STYLES}


class PhosphorIcons(Extension):
    """Install with `Citry(extensions=[PhosphorIcons])`."""

    name = "phosphor"

    class Config(Extension.Config):
        default_weight: str = DEFAULT_WEIGHT
        default_style: str = DEFAULT_STYLE

    def validate_config_fields(self, fields: dict[str, Any], *, component: Any = None) -> None:
        for name, value in fields.items():
            if name not in ALLOWED:
                msg = f"unknown config field {name!r}; expected {' or '.join(sorted(ALLOWED))}"
                raise ValueError(msg)
            if value not in ALLOWED[name]:
                msg = f"{name} must be one of {', '.join(sorted(ALLOWED[name]))}; got {value!r}"
                raise ValueError(msg)
