import io

import pytest

from rich.cells import cell_len
from rich.console import Console
from rich.panel import Panel
from rich.segment import Segment
from rich.style import Style
from rich.table import Table
from rich.text import Text

tests = [
    Panel("Hello, World", padding=0),
    Panel("Hello, World", expand=False, padding=0),
    Panel.fit("Hello, World", padding=0),
    Panel("Hello, World", width=8, padding=0),
    Panel(Panel("Hello, World", padding=0), padding=0),
    Panel("Hello, World", title="FOO", padding=0),
    Panel("Hello, World", subtitle="FOO", padding=0),
]

expected = [
    "╭────────────────────────────────────────────────╮\n│Hello, World                                    │\n╰────────────────────────────────────────────────╯\n",
    "╭────────────╮\n│Hello, World│\n╰────────────╯\n",
    "╭────────────╮\n│Hello, World│\n╰────────────╯\n",
    "╭──────╮\n│Hello,│\n│World │\n╰──────╯\n",
    "╭────────────────────────────────────────────────╮\n│╭──────────────────────────────────────────────╮│\n││Hello, World                                  ││\n│╰──────────────────────────────────────────────╯│\n╰────────────────────────────────────────────────╯\n",
    "╭───────────────────── FOO ──────────────────────╮\n│Hello, World                                    │\n╰────────────────────────────────────────────────╯\n",
    "╭────────────────────────────────────────────────╮\n│Hello, World                                    │\n╰───────────────────── FOO ──────────────────────╯\n",
]


def render(panel, width=50) -> str:
    console = Console(file=io.StringIO(), width=width, legacy_windows=False)
    console.print(panel)
    result = console.file.getvalue()
    print(result)
    return result


@pytest.mark.parametrize("panel,expected", list(zip(tests, expected)))
def test_render_panel(panel, expected) -> None:
    assert render(panel) == expected


def test_console_width() -> None:
    console = Console(file=io.StringIO(), width=50, legacy_windows=False)
    panel = Panel("Hello, World", expand=False)
    min_width, max_width = panel.__rich_measure__(console, console.options)
    assert min_width == 16
    assert max_width == 16


def test_fixed_width() -> None:
    console = Console(file=io.StringIO(), width=50, legacy_windows=False)
    panel = Panel("Hello World", width=20)
    min_width, max_width = panel.__rich_measure__(console, console.options)
    assert min_width == 20
    assert max_width == 20


def test_render_size() -> None:
    console = Console(width=63, height=46, legacy_windows=False)
    options = console.options.update_dimensions(80, 4)
    lines = console.render_lines(Panel("foo", title="Hello"), options=options)
    print(repr(lines))
    expected = [
        [
            Segment("╭─", Style()),
            Segment(
                "────────────────────────────────── Hello ───────────────────────────────────"
            ),
            Segment("─╮", Style()),
        ],
        [
            Segment("│", Style()),
            Segment(" ", Style()),
            Segment("foo"),
            Segment(
                "                                                                         ",
                Style(),
            ),
            Segment(" ", Style()),
            Segment("│", Style()),
        ],
        [
            Segment("│", Style()),
            Segment(" ", Style()),
            Segment(
                "                                                                            ",
                Style(),
            ),
            Segment(" ", Style()),
            Segment("│", Style()),
        ],
        [
            Segment(
                "╰──────────────────────────────────────────────────────────────────────────────╯",
                Style(),
            )
        ],
    ]
    assert lines == expected


def test_title_text() -> None:
    panel = Panel(
        "Hello, World",
        title=Text("title", style="red"),
        subtitle=Text("subtitle", style="magenta bold"),
    )
    console = Console(
        file=io.StringIO(),
        width=50,
        height=20,
        legacy_windows=False,
        force_terminal=True,
        color_system="truecolor",
    )
    console.print(panel)

    result = console.file.getvalue()
    print(repr(result))
    expected = "╭────────────────────\x1b[31m title \x1b[0m─────────────────────╮\n│ Hello, World                                   │\n╰───────────────────\x1b[1;35m subtitle \x1b[0m───────────────────╯\n"
    assert result == expected


def test_title_text_with_border_color() -> None:
    """Regression test for https://github.com/Textualize/rich/issues/2745"""
    panel = Panel(
        "Hello, World",
        border_style="blue",
        title=Text("title", style="red"),
        subtitle=Text("subtitle", style="magenta bold"),
    )
    console = Console(
        file=io.StringIO(),
        width=50,
        height=20,
        legacy_windows=False,
        force_terminal=True,
        color_system="truecolor",
    )
    console.print(panel)

    result = console.file.getvalue()
    print(repr(result))
    expected = "\x1b[34m╭─\x1b[0m\x1b[34m───────────────────\x1b[0m\x1b[31m title \x1b[0m\x1b[34m────────────────────\x1b[0m\x1b[34m─╮\x1b[0m\n\x1b[34m│\x1b[0m Hello, World                                   \x1b[34m│\x1b[0m\n\x1b[34m╰─\x1b[0m\x1b[34m──────────────────\x1b[0m\x1b[1;35m subtitle \x1b[0m\x1b[34m──────────────────\x1b[0m\x1b[34m─╯\x1b[0m\n"
    assert result == expected


def test_title_text_with_panel_background() -> None:
    """Regression test for https://github.com/Textualize/rich/issues/3569"""
    panel = Panel(
        "Hello, World",
        style="on blue",
        title=Text("title", style="red"),
        subtitle=Text("subtitle", style="magenta bold"),
    )
    console = Console(
        file=io.StringIO(),
        width=50,
        height=20,
        legacy_windows=False,
        force_terminal=True,
        color_system="truecolor",
    )
    console.print(panel)

    result = console.file.getvalue()
    print(repr(result))
    expected = "\x1b[44m╭─\x1b[0m\x1b[44m───────────────────\x1b[0m\x1b[31;44m title \x1b[0m\x1b[44m────────────────────\x1b[0m\x1b[44m─╮\x1b[0m\n\x1b[44m│\x1b[0m\x1b[44m \x1b[0m\x1b[44mHello, World\x1b[0m\x1b[44m                                  \x1b[0m\x1b[44m \x1b[0m\x1b[44m│\x1b[0m\n\x1b[44m╰─\x1b[0m\x1b[44m──────────────────\x1b[0m\x1b[1;35;44m subtitle \x1b[0m\x1b[44m──────────────────\x1b[0m\x1b[44m─╯\x1b[0m\n"
    assert result == expected


@pytest.mark.parametrize("padding", [0, (0, 1), (0, 3)])
@pytest.mark.parametrize(
    "subtitle,plain,expected_width",
    [
        ("press q to quit", "press q to quit", 21),
        ("[bold]press q to quit[/bold]", "press q to quit", 21),
        (Text("宽度检查", style="bold"), "宽度检查", 14),
        ("go\tback", "go      back", 18),
        ("one\ntwo", "one two", 13),
    ],
)
def test_fit_long_subtitle(padding, subtitle, plain, expected_width) -> None:
    original = subtitle.copy() if isinstance(subtitle, Text) else subtitle
    panel = Panel.fit("x", title="App", subtitle=subtitle, padding=padding)
    console = Console(width=80, legacy_windows=False)
    measurement = console.measure(panel)
    assert measurement.minimum == measurement.maximum == expected_width

    lines = render(panel, width=80).splitlines()
    assert lines[-1] == f"╰─ {plain} ─╯"
    assert all(cell_len(line) == expected_width for line in lines)
    assert subtitle == original


@pytest.mark.parametrize(
    "width,expected_footer",
    [
        (4, "╰──╯"),
        (8, "╰─ pre─╯"),
        (12, "╰─ press q─╯"),
        (20, "╰─ press q to quit─╯"),
        (21, "╰─ press q to quit ─╯"),
    ],
)
def test_fit_subtitle_narrow_console(width, expected_footer) -> None:
    panel = Panel.fit("x", subtitle="press q to quit")
    lines = render(panel, width=width).splitlines()
    assert lines[-1] == expected_footer
    assert all(cell_len(line) == width for line in lines)


@pytest.mark.parametrize("width", [1, 2, 3])
def test_fit_subtitle_tiny_console(width) -> None:
    panel = Panel.fit("x", subtitle="press q to quit")
    lines = render(panel, width=width).splitlines()
    assert lines
    assert all(cell_len(line) <= width for line in lines)


@pytest.mark.parametrize("padding", [0, (0, 1), (0, 3)])
@pytest.mark.parametrize(
    "width,expected_width,expected_footer",
    [
        (80, 23, "│╰─ press q to quit ─╯│"),
        (12, 12, "│╰─ press─╯│"),
    ],
)
def test_fit_subtitle_nested(padding, width, expected_width, expected_footer) -> None:
    inner = Panel.fit("x", subtitle="press q to quit", padding=padding)
    panel = Panel.fit(inner, padding=0)
    console = Console(width=width, legacy_windows=False)
    measurement = console.measure(panel)
    assert measurement.minimum == measurement.maximum == expected_width

    lines = render(panel, width=width).splitlines()
    assert expected_footer in lines
    assert all(cell_len(line) == expected_width for line in lines)


def test_fit_subtitle_in_table() -> None:
    table = Table.grid(padding=(0, 1))
    table.add_row(Panel.fit("x", subtitle="press q to quit", padding=0), "tail")
    output = render(table, width=80)
    assert "╰─ press q to quit ─╯" in output
    assert "tail" in output


@pytest.mark.parametrize("console_width,expected_width", [(8, 8), (80, 12)])
def test_fit_subtitle_explicit_width(console_width, expected_width) -> None:
    panel = Panel.fit("x", subtitle="press q to quit", width=12)
    console = Console(width=console_width, legacy_windows=False)
    measurement = console.measure(panel)
    assert measurement.minimum == measurement.maximum == expected_width
    lines = render(panel, width=console_width).splitlines()
    assert all(cell_len(line) == expected_width for line in lines)


@pytest.mark.parametrize(
    "content,title",
    [("content longer than the subtitle", None), ("x", "title longer than subtitle")],
)
def test_fit_short_subtitle_preserves_width(content, title) -> None:
    without_subtitle = Panel.fit(content, title=title)
    with_subtitle = Panel.fit(content, title=title, subtitle="q")
    console = Console(width=80, legacy_windows=False)
    assert console.measure(with_subtitle) == console.measure(without_subtitle)
    assert (
        render(with_subtitle, width=80).splitlines()[:-1]
        == render(without_subtitle, width=80).splitlines()[:-1]
    )


if __name__ == "__main__":
    expected = []
    for panel in tests:
        result = render(panel)
        print(result)
        expected.append(result)
    print("--")
    print()
    print(f"expected={repr(expected)}")
