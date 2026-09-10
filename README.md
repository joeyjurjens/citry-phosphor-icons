# citry-phosphor-icons

[Phosphor Icons](https://phosphoricons.com) as [citry](https://citry.dev) components.

[Browse all icons →](https://joeyjurjens.github.io/py-phosphor-icons/preview.html)

## Install

```bash
pip install citry-phosphor-icons
```

The library configures itself through a citry extension, so install both:

```python
import citry_phosphor_icons
from citry import Citry
from citry_phosphor_icons import PhosphorIcons

app = Citry(extensions=[PhosphorIcons])
app.register_library(citry_phosphor_icons)
```

Registration fails with a clear error if the extension is missing, so the two
cannot drift apart.

## Naming the tag

The component is `<c-icon />`. To publish it under a different tag, install the
manifest that `library()` builds:

```python
app.register_library(citry_phosphor_icons.library("ph-icon"))
```

That gives `<c-ph-icon />` and nothing else. A manifest owns the names it
publishes and citry will not retire one, so this replaces the default rather
than adding to it - install either this package or a named manifest, not both.

To keep `<c-icon />` and answer to a second name as well, alias the installed
class instead:

```python
from citry_phosphor_icons import Icon

installed = app.register_library(citry_phosphor_icons)
app.register(installed.component(Icon), "ph-icon")
```

## Use

```citry-html
<c-icon name="house" />
<c-icon name="house" weight="bold" />
<c-icon name="house" style="stroke" c-size="24" color="#ff0000" />
```

| Kwarg | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | — | Icon name, e.g. `"house"` |
| `weight` | `str` | engine default | `bold`, `duotone`, `fill`, `light`, `regular`, `thin` |
| `style` | `str` | engine default | `flat` or `stroke` |
| `size` | `str` or `int` | `None` | Sets width and height; any CSS length (`"1.5rem"`), an `int` is read as px |
| `color` | `str` | `None` | Sets CSS `color` |
| `mirrored` | `bool` | `False` | Flips the icon horizontally |
| `attrs` | `dict` | `None` | Extra attributes passed to the `<svg>` element |

`class` and `style` from `attrs` are combined with the component's own, not
replaced by them - so passing `c-attrs="{'class': 'me-2'}"` keeps whatever the
component already sets, and `size` still wins over a conflicting `width`.

## Settings

Defaults belong to the engine, not the process, so two `Citry` instances can
differ:

```python
app = Citry(
    extensions=[PhosphorIcons],
    extensions_defaults={"phosphor": {"default_weight": "bold", "default_style": "stroke"}},
)
```

A caller's keyword argument beats the engine default, and a component may pin
its own. Because a library definition cannot carry engine-specific fields, pin
it on the installed class:

```python
installed = app.register_library(citry_phosphor_icons)


class ThinIcon(installed.component(Icon)):
    class Phosphor:
        default_weight = "thin"
```

Unknown fields and invalid values are rejected when the engine is built, not at
the first render.

Rendering is cached per unique set of keyword arguments. Citry reads
`Cache.enabled` as a literal on the component class, so turning it off is a
property of the manifest rather than an engine setting:

```python
app.register_library(citry_phosphor_icons.library(cache=False))
```

## Subclassing

`Kwargs` is inherited, so a subclass only declares what it changes.
`get_attrs()` returns what the component sets on the `<svg>` itself,
`get_default_attrs()` what the caller's `attrs` may override. Subclass the
definition and ship it as your own library:

```python
from citry import ComponentLibrary, merge_attrs
from citry_phosphor_icons import Icon


class MyIcon(Icon):
    def get_attrs(self, kwargs):
        return merge_attrs({"class": "icon"}, super().get_attrs(kwargs))


__citry_library__ = ComponentLibrary(
    name="my-icons",
    components=(MyIcon,),
    required_extensions=("phosphor",),
)
```

## Previews

The component ships examples for citry's preview extension: one per weight and
style, plus the presentation arguments. `preview_app.py` in this repository
wires an engine for it:

```sh
uv run citry --app preview_app:app ext run preview serve
```

Open the printed gallery URL. Variants are plain keyword arguments rather than
a preview template, so they keep working under a different tag name.

An icon carries no width or height of its own - it takes the size of its
surroundings, like a letter does. Every variant therefore asks for a `size`,
and the preview frame is only a little larger.

The gallery documents the component. For the icon set itself, browse the
[catalogue](https://joeyjurjens.github.io/py-phosphor-icons/preview.html) in
py-phosphor-icons, which has search, a size slider and a colour picker across
all 1512 icons in every weight and style.

## Search and metadata

The icons, the loader and search over the icon metadata live in
[py-phosphor-icons](https://github.com/joeyjurjens/py-phosphor-icons), which this
package builds on:

```python
from py_phosphor_icons import get_svg, get_svg_inner, icon_names, search_icons

search_icons("arrow left")  # ranked, best match first
search_icons("roledex")  # matches on tags: address-book
get_svg("house", weight="bold")
```

The same search answers a wrong `name`, so `<c-icon name="cart" />` raises
`Did you mean: shopping-cart, shopping-cart-simple, car?`, narrowed to icons
that exist in the requested weight and style.

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format .
```

The icon set and its metadata are maintained in
[py-phosphor-icons](https://github.com/joeyjurjens/py-phosphor-icons); the sync
scripts live there.

## Known icon issues

A few icons are incomplete in the upstream Phosphor release and fail to render
in certain weight and style combinations. The current list is maintained in
[py-phosphor-icons](https://github.com/joeyjurjens/py-phosphor-icons#known-icon-issues),
which is where the icon set is synced.
