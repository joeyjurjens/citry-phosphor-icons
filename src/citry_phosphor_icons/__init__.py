"""citry-phosphor-icons"""

from citry import Citry, ComponentLibrary, LibraryInstallation
from py_phosphor_icons import DEFAULT_STYLE, DEFAULT_WEIGHT, VALID_STYLES, VALID_WEIGHTS

from citry_phosphor_icons.components.icon import Icon

#: The tag the component is published under unless `install()` is told otherwise.
DEFAULT_NAME = "icon"

__citry_library__ = ComponentLibrary(name="citry-phosphor-icons", components=(Icon,))


def library(
    name: str = DEFAULT_NAME,
    *,
    weight: str = DEFAULT_WEIGHT,
    style: str = DEFAULT_STYLE,
    cache: bool = True,
    override: type[Icon] | None = None,
) -> ComponentLibrary:
    """The manifest, publishing `override or Icon` under `name`.

    Nothing here references the component by name, so the tag is free - a
    library whose components render each other publishes a fixed prefix
    instead. `weight` and `style` become the component's own defaults, which a
    caller's keyword argument still beats.
    """
    for field, value, allowed in (
        ("weight", weight, VALID_WEIGHTS),
        ("style", style, VALID_STYLES),
    ):
        if value not in allowed:
            msg = f"{field} must be one of {', '.join(sorted(allowed))}; got {value!r}"
            raise ValueError(msg)

    unchanged = (
        name == DEFAULT_NAME
        and weight == DEFAULT_WEIGHT
        and style == DEFAULT_STYLE
        and cache
        and override is None
    )
    if unchanged:
        return __citry_library__

    base = override or Icon
    definition = type(
        base.__name__,
        (base,),
        {
            "name": name,
            "Kwargs": type(
                "Kwargs",
                (),
                {
                    "__annotations__": {"weight": str, "style": str},
                    "weight": weight,
                    "style": style,
                },
            ),
            "Cache": type("Cache", (), {"enabled": cache}),
        },
    )
    return ComponentLibrary(name="citry-phosphor-icons", components=(definition,))


def install(
    app: Citry,
    *,
    name: str = DEFAULT_NAME,
    weight: str = DEFAULT_WEIGHT,
    style: str = DEFAULT_STYLE,
    cache: bool = True,
    override: type[Icon] | None = None,
) -> LibraryInstallation:
    """Register the library.

    The component is published as `<c-icon />`, drawing regular flat icons:

        install(app, name="ph-icon", weight="bold", override=MyIcon)
    """
    return app.register_library(
        library(name, weight=weight, style=style, cache=cache, override=override)
    )


__all__ = ["DEFAULT_NAME", "Icon", "__citry_library__", "install", "library"]
