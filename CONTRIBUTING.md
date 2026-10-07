# Contributing

Thanks for helping to keep these specifications accurate.

## Reporting a difference

If a real response does not match the spec, open an issue with:

- the operation (for example `GET /v1/events/...`) and the line type and language used;
- the field or behaviour that differs, and a minimal, anonymised JSON excerpt.

**Never post an API key, JWT, password, callback secret or your personal base URL.**

## Changing the specs

The specs are hand-maintained YAML files in `openapi/`. The source of truth is the
[SportAPI documentation](https://sportapi.net/docs.html): please do not add endpoints, fields or limits
that are not documented there. Keep examples realistic and small (trim long arrays).

Before opening a pull request, run the checks that CI runs:

```bash
pip install -r requirements-dev.txt
make check
```

If you change `openapi/sport-line-api.yaml`, regenerate the Postman collection with `make postman`
and commit the result.
