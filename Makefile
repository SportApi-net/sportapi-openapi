SPECS := openapi/sport-line-api.yaml openapi/coupon-api.yaml

.PHONY: check validate examples lint postman

## check: run every check that CI runs
check: validate examples lint

## validate: validate both documents against the OpenAPI 3.0 schema
validate:
	openapi-spec-validator $(SPECS)

## examples: validate every example against its schema
examples:
	python3 scripts/check_examples.py $(SPECS)

## lint: Redocly recommended rules (needs Node.js)
lint:
	npx --yes @redocly/cli@2 lint

## postman: regenerate the Postman collection (needs Node.js)
postman:
	./scripts/build_postman.sh
