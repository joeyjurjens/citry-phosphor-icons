from typing import Any

from citry import LibraryComponent, Markup, merge_attrs
from py_phosphor_icons import VALID_STYLES, VALID_WEIGHTS, get_svg_inner, validate

from citry_phosphor_icons.preview import SIZE, weight_and_style_variants


def _viewport():
    """A frame just larger than the icon; the preview extension is optional."""
    try:
        from citry.ext.preview import Viewport
    except ImportError:
        return None
    return Viewport(width=SIZE * 3, height=SIZE * 2)


class Icon(LibraryComponent):
    class Cache:
        enabled = True

    class Preview:
        group = "Phosphor"
        viewport = _viewport()

        def variants(self):
            return weight_and_style_variants(VALID_WEIGHTS, VALID_STYLES)

    class Kwargs:
        name: str
        # The engine's `phosphor` config supplies these; see extension.py.
        weight: str | None = None
        style: str | None = None
        size: str | int | None = None
        color: str | None = None
        mirrored: bool = False
        attrs: dict[str, Any] | None = None

    def resolve(self, kwargs: "Icon.Kwargs") -> tuple[str, str]:
        """The weight and style to render: the caller's, else the engine's.

        A value that came from a template attribute is a sandbox proxy that
        only impersonates `str`; `pathlib` on Python 3.12+ rejects it. The
        strings leave the sandbox here, before any plain Python sees them.
        """
        return (
            str(kwargs.weight or self.phosphor.default_weight),
            str(kwargs.style or self.phosphor.default_style),
        )

    def get_attrs(self, kwargs: "Icon.Kwargs") -> dict[str, Any]:
        """Attributes the component sets itself. Merged over the caller's `attrs`,
        so `class` and `style` are appended to it rather than replaced by it."""
        style = []
        if kwargs.size:
            size = f"{kwargs.size}px" if isinstance(kwargs.size, int) else kwargs.size
            style.append(f"width: {size}; height: {size};")
        if kwargs.color:
            style.append(f"color: {kwargs.color};")
        if kwargs.mirrored:
            style.append("transform: scaleX(-1);")

        return {"style": " ".join(style)} if style else {}

    def get_default_attrs(self, weight: str, style: str) -> dict[str, Any]:
        """Attributes the caller's `attrs` may override."""
        attrs = {
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": "0 0 256 256",
            "aria-hidden": "true",
        }
        if style == "flat" or weight == "fill":
            attrs["fill"] = "currentColor"
        return attrs

    def template_data(self, kwargs: "Icon.Kwargs", slots) -> dict:
        weight, style = self.resolve(kwargs)
        validate(weight, style)
        data = {
            "svg_inner": get_svg_inner(str(kwargs.name), weight, style),
            "attrs": merge_attrs(kwargs.attrs or {}, self.get_attrs(kwargs)),
            "default_attrs": self.get_default_attrs(weight, style),
        }
        data["svg_attrs"] = merge_attrs((data["attrs"] or {}), (data["default_attrs"] or {}))
        data["Markup"] = Markup
        return data

    template = """
        <svg c-bind="svg_attrs">
        <c-slot name="title"></c-slot>{{ Markup(svg_inner) }}
        </svg>
    """
