"""citry-phosphor-icons"""

from citry import ComponentLibrary

from citry_phosphor_icons.components.icon import Icon
from citry_phosphor_icons.extension import PhosphorIcons

DEFAULT_NAME = "icon"

__citry_library__ = ComponentLibrary(
    name="citry-phosphor-icons",
    components=(Icon,),
    required_extensions=("phosphor",),
)


def library(name: str = DEFAULT_NAME, *, cache: bool = True) -> ComponentLibrary:
    """The manifest, with the component registered under `name`.

    A manifest owns the names it publishes and citry will not retire one, so
    choosing a different tag means installing a different manifest rather than
    renaming afterwards:

        app.register_library(citry_phosphor_icons.library("ph-icon"))

    gives `<c-ph-icon />` and nothing else. Citry reads `Cache.enabled` as a
    literal on the class, which is why turning caching off is a property of the
    manifest too rather than an engine setting.
    """
    if name == DEFAULT_NAME and cache:
        return __citry_library__
    definition = type(
        "Icon",
        (Icon,),
        {"name": name, "Cache": type("Cache", (), {"enabled": cache})},
    )
    return ComponentLibrary(
        name="citry-phosphor-icons",
        components=(definition,),
        required_extensions=("phosphor",),
    )


__all__ = ["DEFAULT_NAME", "Icon", "PhosphorIcons", "__citry_library__", "library"]
