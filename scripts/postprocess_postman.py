#!/usr/bin/env python3
"""Make the generated Postman collection ready to use and stable in git.

- declares the `apiKey` collection variable used by the `Package` header auth;
- documents the `baseUrl` variable;
- replaces the random `_postman_id` with a fixed one so regenerating does not create noise.
"""
import json
import sys



def main(src, dst):
    with open(src, encoding="utf-8") as fh:
        collection = json.load(fh)

    collection["info"]["_postman_id"] = "0b0c6f5e-3f7a-4a51-9d55-2f6a1c0e5a01"
    variables = {v["key"]: v for v in collection.get("variable", [])}
    variables["baseUrl"] = {
        "key": "baseUrl",
        "value": variables.get("baseUrl", {}).get("value", "https://YOUR_API_DOMAIN"),
        "type": "string",
        "description": "Your personal Sport Line API base URL from the SportAPI manager, without a trailing slash.",
    }
    variables["apiKey"] = {
        "key": "apiKey",
        "value": "",
        "type": "secret",
        "description": "Your API key. It is sent in the `Package` header. Do not commit it or share exported collections that contain it.",
    }
    collection["variable"] = [variables["baseUrl"], variables["apiKey"]]

    with open(dst, "w", encoding="utf-8") as fh:
        json.dump(collection, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    main(*sys.argv[1:3])
