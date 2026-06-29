#!/usr/bin/env python3
"""Glossary CLI — manage a project's ubiquitous language glossary."""

import argparse
import json
import os
import sys

# Ensure sibling modules are importable regardless of invocation directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config, write_config, ConfigError
from store import load_store, save_store, search_term, add_term, update_term, delete_term, list_terms, list_all_terms, list_categories
from renderer import write_markdown


def out(status, data):
    """Write structured JSON result to stdout."""
    print(json.dumps({"status": status, "data": data}))


def err(message):
    """Write plain-text error to stderr."""
    print(message, file=sys.stderr)


def get_config():
    """Load config or exit 1 with error."""
    try:
        return load_config()
    except ConfigError as e:
        err(str(e))
        sys.exit(1)


# --- command handlers ---

def cmd_init(args):
    try:
        write_config(args.json_path, args.markdown_path)
    except ConfigError as e:
        err(str(e))
        sys.exit(1)
    if not os.path.exists(args.json_path):
        save_store(args.json_path, {"categories": {}})
    out("ok", {"message": ".glossaryrc created successfully."})


def cmd_search(args):
    config = get_config()
    data = load_store(config["json_path"])
    term, _ = search_term(data, args.term)
    if term is None:
        err(f"Term not found: {args.term}")
        sys.exit(1)
    out("ok", term)


def cmd_add(args):
    config = get_config()
    data = load_store(config["json_path"])
    term_dict = {
        "term": args.term,
        "definition": args.definition,
        "examples": args.examples,
        "synonyms": args.synonyms,
        "related": args.related,
    }
    status, result = add_term(data, args.category, term_dict)
    if status == "conflict":
        err(f"Term already exists: {args.term}")
        out("conflict", result)
        sys.exit(2)
    save_store(config["json_path"], result)
    write_markdown(config["markdown_path"], result)
    out("ok", {"message": f"Term '{args.term}' added to '{args.category}'."})


def cmd_update(args):
    config = get_config()
    data = load_store(config["json_path"])
    updates = {}
    if args.category is not None:
        updates["category"] = args.category
    if args.definition is not None:
        updates["definition"] = args.definition
    if args.examples is not None:
        updates["examples"] = args.examples
    if args.synonyms is not None:
        updates["synonyms"] = args.synonyms
    if args.related is not None:
        updates["related"] = args.related
    if not updates:
        err("No fields provided to update. Use at least one of: --category, --definition, --examples, --synonyms, --related")
        sys.exit(1)
    found, result = update_term(data, args.term, updates)
    if not found:
        err(f"Term not found: {args.term}")
        sys.exit(1)
    save_store(config["json_path"], result)
    write_markdown(config["markdown_path"], result)
    out("ok", {"message": f"Term '{args.term}' updated."})


def cmd_delete(args):
    config = get_config()
    data = load_store(config["json_path"])
    found, result = delete_term(data, args.term)
    if not found:
        err(f"Term not found: {args.term}")
        sys.exit(1)
    save_store(config["json_path"], result)
    write_markdown(config["markdown_path"], result)
    out("ok", {"message": f"Term '{args.term}' deleted."})


def cmd_list(args):
    config = get_config()
    data = load_store(config["json_path"])
    terms = list_terms(data, args.category)
    if terms is None:
        err(f"Category not found: {args.category}")
        sys.exit(1)
    out("ok", terms)


def cmd_list_all(args):
    config = get_config()
    data = load_store(config["json_path"])
    out("ok", list_all_terms(data))


def cmd_categories(args):
    config = get_config()
    data = load_store(config["json_path"])
    out("ok", list_categories(data))


def cmd_render(args):
    config = get_config()
    data = load_store(config["json_path"])
    write_markdown(config["markdown_path"], data)
    out("ok", {"message": "Glossary.md regenerated."})


# --- parser setup ---

def build_parser():
    parser = argparse.ArgumentParser(
        prog="glossary.py",
        description=(
            "Glossary CLI — manage a project's ubiquitous language glossary.\n\n"
            "Reads .glossaryrc from the current directory to locate glossary.json\n"
            "and Glossary.md. Run 'init' first to set up a new project.\n\n"
            "All successful output is JSON on stdout.\n"
            "All errors are plain text on stderr.\n\n"
            "Exit codes:\n"
            "  0  success\n"
            "  1  not found / general error / missing .glossaryrc\n"
            "  2  conflict (duplicate term on add)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # init
    p_init = sub.add_parser("init", help="Set up glossary for a project")
    p_init.add_argument("--json-path", required=True, metavar="<path>", help="Absolute path to glossary.json")
    p_init.add_argument("--markdown-path", required=True, metavar="<path>", help="Absolute path to Glossary.md")

    # search
    p_search = sub.add_parser("search", help="Look up a term by name")
    p_search.add_argument("term", metavar="<term>", help="Term name to search for")

    # add
    p_add = sub.add_parser("add", help="Add a new term")
    p_add.add_argument("--term", required=True, metavar="<name>")
    p_add.add_argument("--category", required=True, metavar="<category>")
    p_add.add_argument("--definition", required=True, metavar="<text>")
    p_add.add_argument("--examples", required=True, metavar="<text>")
    p_add.add_argument("--synonyms", required=True, metavar="<text>")
    p_add.add_argument("--related", required=True, metavar="<text>")

    # update
    p_update = sub.add_parser("update", help="Update fields on an existing term (partial patch)")
    p_update.add_argument("--term", required=True, metavar="<name>")
    p_update.add_argument("--category", default=None, metavar="<category>", help="Move term to a different category")
    p_update.add_argument("--definition", default=None, metavar="<text>")
    p_update.add_argument("--examples", default=None, metavar="<text>")
    p_update.add_argument("--synonyms", default=None, metavar="<text>")
    p_update.add_argument("--related", default=None, metavar="<text>")

    # delete
    p_delete = sub.add_parser("delete", help="Delete a term")
    p_delete.add_argument("--term", required=True, metavar="<name>")

    # list
    p_list = sub.add_parser("list", help="List all term names in a category")
    p_list.add_argument("--category", required=True, metavar="<category>")

    # list-all
    sub.add_parser("list-all", help="List all terms grouped by category")

    # categories
    sub.add_parser("categories", help="List all category names")

    # render
    sub.add_parser("render", help="Regenerate Glossary.md from glossary.json")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    dispatch = {
        "init": cmd_init,
        "search": cmd_search,
        "add": cmd_add,
        "update": cmd_update,
        "delete": cmd_delete,
        "list": cmd_list,
        "list-all": cmd_list_all,
        "categories": cmd_categories,
        "render": cmd_render,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
