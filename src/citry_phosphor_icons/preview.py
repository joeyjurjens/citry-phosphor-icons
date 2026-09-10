"""Examples for citry's preview extension.

Every variant is plain keyword arguments rather than a preview template, so the
gallery does not depend on the tag the component happens to be registered under.

The whole icon set is a catalogue rather than a set of examples; browse it at
py-phosphor-icons instead. What is worth seeing side by side is how one icon
changes across weights, styles, and the presentation arguments.
"""

from collections.abc import Iterable

SAMPLE = "house"

# An icon carries no width or height of its own -- it takes the size of its
# surroundings, like a letter does. A preview frame is that surrounding, so
# every variant asks for a size and the frame is only a little larger.
SIZE = 96


def weight_and_style_variants(weights: Iterable[str], styles: Iterable[str]) -> list:
    from citry.ext.preview import variant

    variants = [
        variant(
            slug=f"{style}-{weight}",
            label=f"{weight.title()}, {style}",
            params={"name": SAMPLE, "weight": weight, "style": style, "size": SIZE},
        )
        for style in sorted(styles)
        for weight in sorted(weights)
    ]
    variants += [
        variant(
            slug="sized",
            label="Sized",
            description="`size` sets width and height; an int is read as px.",
            params={"name": SAMPLE, "size": 192},
        ),
        variant(
            slug="colored",
            label="Coloured",
            description="`color` sets CSS color; the SVG uses currentColor.",
            params={"name": SAMPLE, "color": "#c0392b", "size": SIZE},
        ),
        variant(
            slug="mirrored",
            label="Mirrored",
            params={"name": "arrow-right", "mirrored": True, "size": SIZE},
        ),
        variant(
            slug="extra-attributes",
            label="Extra attributes",
            description="`attrs` is merged, so class and style are appended.",
            params={
                "name": SAMPLE,
                "size": SIZE,
                "attrs": {"class": "shadow", "aria-label": "Home"},
            },
        ),
    ]
    return variants
