# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-10-07

### Added

- `openapi/sport-line-api.yaml` — OpenAPI 3.0.3 description of the SportAPI Sport Line API: 12
  operations (`menu`, `events`, the match calendar, `event`, `search`, `sports`, `countries`,
  `tournaments`, `toplist`, `topmatches`, `topchampionships`, `account`), the `Package` header
  security scheme, the `X-Key-Expires` response header, documented errors and `event` service
  messages, and trimmed real response examples.
- `openapi/coupon-api.yaml` — OpenAPI 3.0.3 description of the SportAPI Coupon API: health check,
  login, coupon placement, coupon reads, balance, business errors and the signed `coupons.settled`
  callback.
- Postman collection generated from the Sport Line spec.
- `scripts/check_examples.py` — validates every example against its schema.
- CI: openapi-spec-validator, example validation and Redocly lint.
