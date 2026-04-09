HEADER = "<!-- AUTO-GENERATED — do not edit. Use the glossary CLI to make changes. -->\n\n"


def render_markdown(data):
    parts = [HEADER]
    for cat_name in sorted(data["categories"]):
        cat = data["categories"][cat_name]
        parts.append(f"## {cat_name}\n\n")
        for term_name in sorted(cat["terms"]):
            term = cat["terms"][term_name]
            parts.append(f"### {term_name}\n\n")
            parts.append(f"**Term:** {term.get('term', '')}\n\n")
            parts.append(f"**Definition:** {term.get('definition', '')}\n\n")
            parts.append(f"**Examples:** {term.get('examples', '')}\n\n")
            parts.append(f"**Synonyms:** {term.get('synonyms', '')}\n\n")
            parts.append(f"**Related:** {term.get('related', '')}\n\n")
            parts.append("---\n\n")
    return "".join(parts)


def write_markdown(markdown_path, data):
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(render_markdown(data))
