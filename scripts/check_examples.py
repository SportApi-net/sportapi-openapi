#!/usr/bin/env python3
"""Validate every example in the OpenAPI documents against its schema.

openapi-spec-validator checks that a document is valid OpenAPI, but it does not check
that the examples match the schemas they illustrate. This script does: it walks every
media type object (responses, request bodies, callbacks) and every parameter that has a
schema and an example, and validates the example with the OpenAPI 3.0 schema dialect
(`nullable`, `oneOf`, `allOf`, formats).

Usage: python scripts/check_examples.py openapi/*.yaml
"""
import sys

import yaml
from openapi_schema_validator import OAS30Validator, oas30_format_checker


def resolve(doc, node):
    """Follow local $ref pointers (only "#/..." references are used in this repository)."""
    while isinstance(node, dict) and "$ref" in node:
        target = doc
        for part in node["$ref"].lstrip("#/").split("/"):
            target = target[part]
        node = target
    return node


def validator_for(doc, schema):
    # Embed the whole document as the root so "#/components/..." references resolve.
    root = dict(doc)
    root.update(schema if "$ref" in schema else {"allOf": [schema]})
    return OAS30Validator(root, format_checker=oas30_format_checker)


def iter_examples(doc, node, where):
    node = resolve(doc, node)
    if isinstance(node, dict):
        schema = node.get("schema")
        if isinstance(schema, dict):
            if "example" in node:
                yield where, "example", schema, node["example"]
            for name, example in (node.get("examples") or {}).items():
                example = resolve(doc, example)
                if "value" in example:
                    yield where, name, schema, example["value"]
        for key, value in node.items():
            if key in ("schema", "examples", "example"):
                continue
            yield from iter_examples(doc, value, f"{where}/{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from iter_examples(doc, value, f"{where}/{index}")


def check(path):
    with open(path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    count, failures = 0, 0
    for where, name, schema, value in iter_examples(doc, doc.get("paths", {}), "#/paths"):
        count += 1
        errors = sorted(validator_for(doc, schema).iter_errors(value), key=lambda e: list(e.path))
        if errors:
            failures += 1
            print(f"FAIL {path}: {where} [{name}]")
            for error in errors[:5]:
                location = "/".join(str(p) for p in error.absolute_path) or "(root)"
                print(f"    at {location}: {error.message[:200]}")
    status = "OK" if not failures else "FAILED"
    print(f"{path}: {count} examples checked, {failures} failed — {status}")
    return failures == 0


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    results = [check(path) for path in argv]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
