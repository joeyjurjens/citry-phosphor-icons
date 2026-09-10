import pytest
from py_phosphor_icons import VALID_STYLES, VALID_WEIGHTS, exists, icon_names


def all_icon_combinations():
    return [
        (name, weight, style)
        for name in icon_names()
        for weight in sorted(VALID_WEIGHTS)
        for style in sorted(VALID_STYLES)
    ]


def shipped_combinations():
    return [combo for combo in all_icon_combinations() if exists(*combo)]


def unshipped_combinations():
    """Combinations Phosphor itself is missing - see "Known Icon Issues" in the README."""
    return [combo for combo in all_icon_combinations() if not exists(*combo)]


@pytest.mark.parametrize("name,weight,style", shipped_combinations())
def test_icon_renders(name, weight, style, icon):
    output = icon(name=name, weight=weight, style=style)
    assert "<svg" in output


@pytest.mark.parametrize("name,weight,style", unshipped_combinations())
def test_unshipped_icon_raises_with_suggestions(name, weight, style, icon):
    with pytest.raises(FileNotFoundError) as excinfo:
        icon(name=name, weight=weight, style=style)
    assert name in str(excinfo.value)
