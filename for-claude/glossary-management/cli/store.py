import json
import os


class StoreError(Exception):
    pass


def load_store(json_path):
    if not os.path.exists(json_path):
        return {"categories": {}}
    with open(json_path) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise StoreError(f"glossary.json is not valid JSON: {e}") from e


def save_store(json_path, data):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def search_term(data, term_name):
    """Returns (term_dict_with_category, category_name) or (None, None)."""
    for cat_name, cat in data["categories"].items():
        if term_name in cat["terms"]:
            term = dict(cat["terms"][term_name])
            term["category"] = cat_name
            return term, cat_name
    return None, None


def add_term(data, category, term_dict):
    """Returns ("ok", updated_data) or ("conflict", existing_term_with_category)."""
    term_name = term_dict["term"]
    existing, _ = search_term(data, term_name)
    if existing:
        return "conflict", existing
    if category not in data["categories"]:
        data["categories"][category] = {"terms": {}}
    data["categories"][category]["terms"][term_name] = dict(term_dict)  # store a copy
    return "ok", data


def update_term(data, term_name, updates):
    """Partial patch. Returns (True, data) if found, (False, data) if not."""
    updates = dict(updates)  # don't mutate caller's dict
    updates.pop("term", None)  # term name is the key; renaming via update is not supported
    for cat_name, cat in data["categories"].items():
        if term_name in cat["terms"]:
            term = cat["terms"][term_name]
            new_category = updates.pop("category", None)
            for key, value in updates.items():
                term[key] = value
            if new_category and new_category != cat_name:
                if new_category not in data["categories"]:
                    data["categories"][new_category] = {"terms": {}}
                data["categories"][new_category]["terms"][term_name] = term
                del cat["terms"][term_name]
                if not cat["terms"]:
                    del data["categories"][cat_name]
            return True, data
    return False, data


def delete_term(data, term_name):
    """Returns (True, data) if deleted, (False, data) if not found."""
    for cat_name, cat in data["categories"].items():
        if term_name in cat["terms"]:
            del cat["terms"][term_name]
            if not cat["terms"]:
                del data["categories"][cat_name]
            return True, data
    return False, data


def list_terms(data, category):
    """Returns list of term names or None if category not found."""
    if category not in data["categories"]:
        return None
    return list(data["categories"][category]["terms"].keys())


def list_all_terms(data):
    """Returns dict of category -> list of term names."""
    return {cat: list(terms["terms"].keys()) for cat, terms in data["categories"].items()}


def list_categories(data):
    """Returns list of category names."""
    return list(data["categories"].keys())
