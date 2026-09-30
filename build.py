"""Generate the static HAwiki.cz website from Markdown articles.

Run ``python3 build.py`` from any working directory. Source content lives in
``obsah/``, HTML source templates in ``sablony/`` and shared assets in ``assets/``.
Generated pages and the search index are written to ``dist/``.
"""

import html
import importlib
import json
from pathlib import Path
import shutil
from string import Template
import sys

ROOT = Path(__file__).resolve().parent
OUTPUT_DIRECTORY = ROOT / "dist"
SECTIONS = {
    "zaciname": ("Začínáme", "Váš první krok k pohodlnější domácnosti."),
    "co-chci-usnadnit": ("Co chci usnadnit", "Vyberte si podle běžného života."),
    "co-koupit": ("Co koupit", "Nejdřív potřeba, potom nákup."),
    "navody": ("Návody", "Malé kroky s konkrétním výsledkem."),
    "pomoc": ("Pomoc", "Když něco nefunguje, začněte tady."),
    "dalsi-moznosti": ("Další možnosti", "Rozšíření pro váš další krok."),
}
REQUIRED_METADATA = (
    "title", "description", "cas", "obtiznost", "kontrola_zdroju", "stav",
)
PRACTICAL_ARTICLES = {
    "co-chci-usnadnit/svetla",
    "navody/lampa-vecer",
    "pomoc/zalohovani",
}


def render_template(name: str, **values: str) -> str:
    """Substitute values into an HTML source template.

    Callers escape plain text before passing it here. Rendered Markdown and
    other HTML fragments are intentionally inserted unchanged.
    """
    path = ROOT / "sablony" / f"{name}.html"
    return Template(path.read_text(encoding="utf-8")).substitute(values)


def load_pages() -> list[dict[str, str]]:
    """Read YAML metadata and render each Markdown article with its contents.

    Dependencies can be installed locally in ``.vendor`` or in the active Python
    environment. Missing metadata produces an error identifying the source file.
    """
    sys.path.insert(0, str(ROOT / ".vendor"))
    markdown = importlib.import_module("markdown")
    yaml = importlib.import_module("yaml")
    pages = []

    for path in sorted((ROOT / "obsah").rglob("*.md")):
        _, front_matter, body = path.read_text(encoding="utf-8").split("---", 2)
        metadata = yaml.safe_load(front_matter)
        if not isinstance(metadata, dict):
            raise ValueError(f"{path}: metadata must be a YAML mapping")
        missing = [key for key in REQUIRED_METADATA if key not in metadata]
        if missing:
            raise ValueError(f"{path}: missing metadata: {', '.join(missing)}")

        slug = path.relative_to(ROOT / "obsah").with_suffix("").as_posix()
        converter = markdown.Markdown(
            extensions=["toc", "tables", "fenced_code", "admonition"]
        )
        pages.append({
            **metadata,
            "slug": slug,
            "body": converter.convert(body),
            "toc": converter.toc,
        })

    return pages


def render_cards(pages: list[dict[str, str]]) -> str:
    """Render linked article cards from their display metadata."""
    cards = [
        render_template(
            "card",
            slug=html.escape(page["slug"]),
            difficulty=html.escape(page["obtiznost"]),
            duration=html.escape(page["cas"]),
            title=html.escape(page["title"]),
            description=html.escape(page["description"]),
        )
        for page in pages
    ]
    return '<div class="cards">' + "".join(cards) + "</div>"


def write_page(route: str, title: str, description: str, body: str) -> None:
    """Wrap page content in the common layout and save its UTF-8 index file.

    Routes are relative to the output root. An empty route writes the homepage.
    The canonical origin is taken from ``site.json``.
    """
    config = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    canonical_url = config["url"].rstrip("/") + "/"
    if route:
        canonical_url += route + "/"
    navigation = "".join(
        f'<a href="/{key}/">{html.escape(section[0])}</a>'
        for key, section in list(SECTIONS.items())[:5]
    )
    document = render_template(
        "layout",
        title=html.escape(title),
        description=html.escape(description),
        canonical_url=html.escape(canonical_url),
        navigation=navigation,
        body=body,
    )
    path = OUTPUT_DIRECTORY / route / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8")


def write_articles(pages: list[dict[str, str]]) -> None:
    """Generate an article page with breadcrumbs and a table of contents."""
    for page in pages:
        section = page["slug"].split("/")[0]
        body = render_template(
            "article",
            section=html.escape(section),
            section_title=html.escape(SECTIONS[section][0]),
            difficulty=html.escape(page["obtiznost"]),
            duration=html.escape(page["cas"]),
            title=html.escape(page["title"]),
            description=html.escape(page["description"]),
            review_date=html.escape(page["kontrola_zdroju"]),
            review_status=html.escape(page["stav"]),
            content=page["body"],
            table_of_contents=page["toc"],
        )
        write_page(page["slug"], page["title"], page["description"], body)


def write_sections(pages: list[dict[str, str]]) -> None:
    """Generate a listing page for every configured content section."""
    for key, (title, description) in SECTIONS.items():
        section_pages = [page for page in pages if page["slug"].startswith(key + "/")]
        body = render_template(
            "section",
            title=html.escape(title),
            description=html.escape(description),
            cards=render_cards(section_pages),
        )
        write_page(key, title, description, body)


def write_homepage(pages: list[dict[str, str]]) -> None:
    """Generate the homepage with beginner guides and selected practical articles."""
    body = render_template(
        "home",
        starter_cards=render_cards(
            [page for page in pages if page["slug"].startswith("zaciname/")]
        ),
        practical_cards=render_cards(
            [page for page in pages if page["slug"] in PRACTICAL_ARTICLES]
        ),
    )
    write_page(
        "",
        "Chytrá domácnost začíná jedním krokem",
        "Praktický průvodce Home Assistant pro běžné domácnosti.",
        body,
    )


def write_search(pages: list[dict[str, str]]) -> None:
    """Generate the search page and the article metadata consumed by its script."""
    write_page(
        "hledani", "Hledání", "Najděte návod podle toho, co potřebujete.",
        render_template("search"),
    )
    index = [
        {key: page[key] for key in ("title", "description", "slug")}
        for page in pages
    ]
    (OUTPUT_DIRECTORY / "search.json").write_text(
        json.dumps(index, ensure_ascii=False), encoding="utf-8"
    )


def main() -> None:
    """Build articles, section listings, homepage, search index and shared assets."""
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)
    pages = load_pages()
    write_articles(pages)
    write_sections(pages)
    write_homepage(pages)
    write_search(pages)
    shutil.copytree(ROOT / "assets", OUTPUT_DIRECTORY / "assets", dirs_exist_ok=True)
    print(f"Vytvořeno {len(pages) + len(SECTIONS) + 2} HTML stránek.")


if __name__ == "__main__":
    main()
