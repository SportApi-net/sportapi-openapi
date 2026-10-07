# SportAPI OpenAPI specifications

OpenAPI 3.0 descriptions of the [SportAPI](https://sportapi.net) **Sport Line API** (Prematch and Live
odds, scores and sports data) and **Coupon API** (bet placement and settlement). Generate a client in
any language, import the API into Postman or Insomnia, or run a mock server — all from one file.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenAPI 3.0.3](https://img.shields.io/badge/OpenAPI-3.0.3-6BA539.svg)](https://spec.openapis.org/oas/v3.0.3)
[![CI](https://github.com/SportApi-net/sportapi-openapi/actions/workflows/ci.yml/badge.svg)](https://github.com/SportApi-net/sportapi-openapi/actions/workflows/ci.yml)

> The specifications in this repository are free and MIT-licensed. The SportAPI data service itself is
> commercial: you need a personal base URL and API key to call it (see [Get an API key](#get-an-api-key)).

## What's inside

| File | Description |
|---|---|
| [`openapi/sport-line-api.yaml`](openapi/sport-line-api.yaml) | Sport Line API: 12 operations — navigation, match lists, match calendar, a match with all markets, search, top selections and account |
| [`openapi/coupon-api.yaml`](openapi/coupon-api.yaml) | Coupon API: login, coupon placement, coupon reads, balance, and the signed settlement callback |
| [`postman/sportapi-sport-line-api.postman_collection.json`](postman/sportapi-sport-line-api.postman_collection.json) | Ready-made Postman collection generated from the Sport Line spec |
| [`scripts/check_examples.py`](scripts/check_examples.py) | Validates every example in the specs against its schema (runs in CI) |

Highlights:

- Every documented method, path and query parameter, with descriptions, recommended polling intervals
  and a link to the matching page of the [SportAPI documentation](https://sportapi.net/docs.html).
- Response schemas for the envelope, matches, odds (short and grouped markets), sub-matches, Live
  statistics, group-match plans, coupons, bets and callbacks — including the documented quirks (`oc_size`
  is a number *or* a string, `countryId` vs `sport_id`, `/v1/topmathes`, coupon codes with leading zeros).
- Real response examples: trimmed excerpts of the English JSON responses published with the docs, so mock
  servers and API browsers show realistic data.
- Errors as documented: Sport Line `error_code`/`error_message` payloads and `event` service messages;
  Coupon API business errors returned with HTTP 200 and `code = 0`.

## View the specs

| Spec | Swagger Editor | Redoc |
|---|---|---|
| Sport Line API | [Open](https://editor.swagger.io/?url=https://raw.githubusercontent.com/SportApi-net/sportapi-openapi/main/openapi/sport-line-api.yaml) | [Open](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/SportApi-net/sportapi-openapi/main/openapi/sport-line-api.yaml) |
| Coupon API | [Open](https://editor.swagger.io/?url=https://raw.githubusercontent.com/SportApi-net/sportapi-openapi/main/openapi/coupon-api.yaml) | [Open](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/SportApi-net/sportapi-openapi/main/openapi/coupon-api.yaml) |

Locally, build a static HTML reference: `npx @redocly/cli build-docs openapi/sport-line-api.yaml -o sport-line-api.html`.

## 60-second quick start (no key needed)

Run a mock server that answers with the example data from the spec — handy for building a UI before you
have access. The responses are **demo data** (snapshots from the documentation), not live odds.

```bash
git clone https://github.com/SportApi-net/sportapi-openapi.git
cd sportapi-openapi
npx @stoplight/prism-cli mock openapi/sport-line-api.yaml
```

In another terminal (the mock only checks that the `Package` header is present):

```bash
curl -H "Package: demo" http://127.0.0.1:4010/v1/menu/live/en
curl -H "Package: demo" -H "Prefer: example=line" http://127.0.0.1:4010/v1/event/730321837/group/line/en
```

`Prefer: example=<name>` selects one of the named examples (`live`, `line`, `gameIdFinished`, …).

## Switch to live data

SportAPI has no public sandbox. The SportAPI manager gives you a personal **base URL** and **API key**.
Keep them in environment variables — never in code or in the URL:

```bash
export SPORTAPI_BASE_URL='https://YOUR_API_DOMAIN'   # your personal base URL
export SPORTAPI_KEY='YOUR_API_KEY'

curl --header "Package: $SPORTAPI_KEY" "$SPORTAPI_BASE_URL/v1/menu/live/en"
```

- **Swagger Editor "Try it out"**: set the `baseUrl` server variable and authorize `PackageKey` with your key.
- **Postman**: import the collection, then set the `baseUrl` and `apiKey` collection variables
  (`apiKey` is sent in the `Package` header).
- **Insomnia**: *Import* → the YAML file; set the base URL and add the `Package` header.

For a public website, call the API from your backend so visitors never see the key.

## Generate a client

Any [OpenAPI Generator](https://openapi-generator.tech) target works. The specs are tested with
`python`, `typescript-fetch` and `go` (OpenAPI Generator 7.26).

```bash
npx @openapitools/openapi-generator-cli generate \
  -i openapi/sport-line-api.yaml -g python -o ./generated/python \
  --additional-properties=packageName=sportapi_line
```

```python
import os
import sportapi_line

config = sportapi_line.Configuration(host=os.environ["SPORTAPI_BASE_URL"])
config.api_key["PackageKey"] = os.environ["SPORTAPI_KEY"]

with sportapi_line.ApiClient(config) as client:
    menu = sportapi_line.NavigationApi(client).get_menu(type="live", lang="en")
    for sport in menu.body:
        print(sport.id, sport.name, sport.counter)

    event = sportapi_line.MatchesApi(client).get_event(game_id=746146992, type="live", lang="en")
    match = event.body.actual_instance  # MatchDetail, or EventMessage ("Game id finished")
    print(match)
```

Point `SPORTAPI_BASE_URL` at `http://127.0.0.1:4010` and use any `SPORTAPI_KEY` to run the same code
against the mock server.

## Sport Line API operations

Base URL: your personal URL. Authentication: `Package: <API key>` header.

| Method | Path | Purpose | Docs |
|---|---|---|---|
| GET | `/v1/menu/{type}/{lang}` | Sport → country → tournament hierarchy with match counters | [menu](https://sportapi.net/docs/sport-line/api-reference/menu.html) |
| GET | `/v1/events/{sportId}/{tournamentId}/sub/50/{type}/{lang}` | Matches of a sport or tournament with the main odds | [events](https://sportapi.net/docs/sport-line/api-reference/events.html) |
| GET | `/v1/events/{sportId}/{tournamentId}/sub/50/line/{hours}/{days}/{lang}` | Match calendar: next 2–12 hours, today, or a day up to 5 days ahead | [events by period](https://sportapi.net/docs/sport-line/api-reference/events-by-period.html) |
| GET | `/v1/event/{gameId}/group/{type}/{lang}` | One match or sub-match with the complete market list | [event](https://sportapi.net/docs/sport-line/api-reference/event.html) |
| GET | `/v1/search/{type}/{lang}/{text}` | Search matches by team or participant name | [search](https://sportapi.net/docs/sport-line/api-reference/search.html) |
| GET | `/v1/sports/{type}/{lang}` | Sport list | [sports](https://sportapi.net/docs/sport-line/api-reference/optional-methods/sports.html) |
| GET | `/v1/countries/{sportId}/{type}/{lang}` | Countries of a sport | [countries](https://sportapi.net/docs/sport-line/api-reference/optional-methods/countries.html) |
| GET | `/v1/tournaments/{sportId}/{countryId}/{type}/{lang}` | Tournaments of a sport and country | [tournaments](https://sportapi.net/docs/sport-line/api-reference/optional-methods/tournaments.html) |
| GET | `/v1/toplist/{sportId}/{lang}` | Top Prematch matches of one sport | [toplist](https://sportapi.net/docs/sport-line/api-reference/optional-methods/toplist.html) |
| GET | `/v1/topmatches/{type}/{lang}` | Top matches across all sports | [topmatches](https://sportapi.net/docs/sport-line/api-reference/optional-methods/topmatches.html) |
| GET | `/v1/topchampionships/{type}/{lang}` | Popular championships | [topchampionships](https://sportapi.net/docs/sport-line/api-reference/optional-methods/topchampionships.html) |
| GET | `/v1/account` | The client's keys, access period and usage | [account](https://sportapi.net/docs/sport-line/api-reference/optional-methods/account.html) |

`type` is `live` (in progress) or `line` (Prematch). The core flow is `menu → events → event`; see
[Core Concepts](https://sportapi.net/docs/sport-line/getting-started/core-concepts.html) and the
[data models](https://sportapi.net/docs/sport-line/data-models/match.html).

## Coupon API operations

Base URL: issued by the manager. Authentication: `Authorization: Bearer <client JWT>` from `login`.

| Method | Path | Purpose | Docs |
|---|---|---|---|
| GET | `/api/partner/health` | Availability check (no auth) | [endpoints](https://sportapi.net/docs/coupon/reference/endpoints.html) |
| POST | `/api/partner/login` | Obtain a client JWT (no auth) | [authentication](https://sportapi.net/docs/coupon/getting-started/authentication.html) |
| POST | `/api/partner/coupons/place` | Place a single, an accumulator or several singles | [place coupon](https://sportapi.net/docs/coupon/bet-placement/place-coupon.html) |
| GET | `/api/partner/coupons/get` | One coupon by `coupon_code` | [get coupon](https://sportapi.net/docs/coupon/coupons/get-coupon.html) |
| POST | `/api/partner/coupons/results` | Coupons by codes or by placement period | [query results](https://sportapi.net/docs/coupon/coupons/query-results.html) |
| GET | `/api/partner/coupons/calculated` | Coupons settled in the last N minutes | [active and calculated](https://sportapi.net/docs/coupon/coupons/active-and-calculated.html) |
| GET | `/api/partner/coupons/active` | All active coupons | [active and calculated](https://sportapi.net/docs/coupon/coupons/active-and-calculated.html) |
| GET | `/api/partner/balance` | Client account balance | [endpoints](https://sportapi.net/docs/coupon/reference/endpoints.html) |
| POST | `{callback_url}` *(callback)* | Signed settlement snapshot sent to your server | [callbacks](https://sportapi.net/docs/coupon/settlement/callbacks.html) |

Legacy routes and the experimental cashout endpoint are intentionally not described — see
[Compatible Legacy Routes](https://sportapi.net/docs/coupon/reference/legacy-api.html).

## Modelling notes

- **Sport Line errors** are returned as `{"error_code", "error_message"}`. The documentation does not
  define their HTTP status codes, so they are described as the `default` response. Check the parsed JSON
  for `error_code` rather than relying on the status.
- **`event` can return a message instead of a match** (`Game not found`, `Game id finished`); its `body`
  is `oneOf` `MatchDetail` / `EventMessage`.
- **`topmatches` and `toplist`** return short summaries by default and extended objects with
  `full=true`; items are `anyOf` `MatchSummary` / `MatchListItem`.
- **Coupon API business errors** come with HTTP 200 and `code = 0`; each 200 response is `oneOf` the
  success envelope (`code = 1`) and `BusinessError` (`code = 0`).
- Where the docs give a value range rather than a strict limit (for example `time` in
  `/coupons/calculated` is clamped to 120 by the server), the spec describes it instead of rejecting it.

## Validate locally

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
make check            # openapi-spec-validator + example validation + Redocly lint (needs Node.js)
make postman          # regenerate the Postman collection
```

## Documentation

- [SportAPI documentation](https://sportapi.net/docs.html)
- [Sport Line API quick start](https://sportapi.net/docs/sport-line/getting-started/quick-start.html) ·
  [authentication and access](https://sportapi.net/docs/sport-line/getting-started/authentication-and-access.html) ·
  [error handling](https://sportapi.net/docs/sport-line/getting-started/error-handling.html) ·
  [update guidelines](https://sportapi.net/docs/sport-line/getting-started/update-guidelines.html) ·
  [odds and markets](https://sportapi.net/docs/sport-line/data-models/odds.html)
- [Coupon API quick integration](https://sportapi.net/docs/coupon/quick-integration.html) ·
  [bet pointer](https://sportapi.net/docs/coupon/bet-placement/bet-pointer.html) ·
  [statuses and payouts](https://sportapi.net/docs/coupon/settlement/statuses-and-payouts.html) ·
  [callback signature](https://sportapi.net/docs/coupon/settlement/callback-signature.html)

## Get an API key

SportAPI is a commercial data service: plans start from $30/month, and there is a free 2-day trial.

- Request a key from the SportAPI manager on Telegram: [@sportapinet_bot](https://t.me/sportapinet_bot?start=github_sportapi_openapi)
- Products: [Sport Line API](https://sportapi.net/sport-line-api.html) ·
  [bet placement and settlement](https://sportapi.net/sport-events-api.html) ·
  [results API](https://sportapi.net/sport-rezult-api.html)
- Website: [sportapi.net](https://sportapi.net)

## Contributing

Issues and pull requests are welcome — especially reports of differences between the specs and real
responses. See [CONTRIBUTING.md](CONTRIBUTING.md). Never include API keys, tokens or callback secrets in
issues, examples or commits.

## License

[MIT](LICENSE) © 2026 SportAPI. The license covers the files in this repository, not access to the
SportAPI service.
