#!/usr/bin/env bash
# Regenerate the Postman collection from the Sport Line API description.
# Requires Node.js (npx) and Python 3.
set -euo pipefail

cd "$(dirname "$0")/.."

OUT=postman/sportapi-sport-line-api.postman_collection.json
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

npx --yes -p openapi-to-postmanv2@6 openapi2postmanv2 \
  -s openapi/sport-line-api.yaml \
  -o "$TMP" \
  -O folderStrategy=Tags,parametersResolution=Example,enableOptionalParameters=false

python3 scripts/postprocess_postman.py "$TMP" "$OUT"
echo "Written $OUT"
