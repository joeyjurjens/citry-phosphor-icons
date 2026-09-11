# citry-phosphor-icons

[Phosphor Icons](https://phosphoricons.com) as [citry](https://citry.dev) components.

[Browse all icons →](https://joeyjurjens.github.io/py-phosphor-icons/preview.html)

## Install

```bash
pip install citry-phosphor-icons
```

```python
import citry_phosphor_icons
from citry import Citry

app = Citry()
citry_phosphor_icons.install(app)
```

Everything else is an argument to that one call:

```python
citry_phosphor_icons.install(
    app,
    name="ph-icon",  # publish as <c-ph-icon /> instead of <c-icon />
    weight="bold",  # the default weight, which a caller still overrides
    style="stroke",
    cache=False,
    override=MyIcon,  # publish your own subclass in its place
)
```

An invalid weight or style is rejected there, not at the first render.

## Use

```citry-html
<c-icon name="house" />
<c-icon name="house" weight="bold" />
<c-icon name="house" style="stroke" c-size="24" color="#ff0000" />
```

| Kwarg | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | - | Icon name, e.g. `"house"` |
| `weight` | `str` | `regular`, or what `install()` set | `bold`, `duotone`, `fill`, `light`, `regular`, `thin` |
| `style` | `str` | `flat`, or what `install()` set | `flat` or `stroke` |
| `size` | `str` or `int` | `None` | Sets width and height; any CSS length (`"1.5rem"`), an `int` is read as px |
| `color` | `str` | `None` | Sets CSS `color` |
| `mirrored` | `bool` | `False` | Flips the icon horizontally |
| `attrs` | `dict` | `None` | Extra attributes passed to the `<svg>` element |

`class` and `style` from `attrs` are combined with the component's own, not
replaced by them - so passing `c-attrs="{'class': 'me-2'}"` keeps whatever the
component already sets, and `size` still wins over a conflicting `width`.

## Replacing the component

`Kwargs` is inherited, so a subclass only declares what it changes.
`get_attrs()` returns what the component sets on the `<svg>` itself,
`get_default_attrs()` what the caller's `attrs` may override:

```python
from citry import merge_attrs
from citry_phosphor_icons import Icon


class MyIcon(Icon):
    def get_attrs(self, kwargs):
        return merge_attrs({"class": "icon"}, super().get_attrs(kwargs))


citry_phosphor_icons.install(app, override=MyIcon)
```

Yours is published under the same tag, so nothing that renders `<c-icon />`
has to change.

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
