# Xquik Apify Actor Backend

Use this backend for structured public X data when `APIFY_TOKEN` is available.
It supplements the existing direct X API workflow.

## Actors

| Actor | Store | Stable Actor ID | API Actor ID |
|---|---|---|---|
| X Tweet Scraper | [Actor listing](https://apify.com/xquik/x-tweet-scraper) | `wAusCMrm284Voaw86` | `xquik~x-tweet-scraper` |
| X Follower Scraper | [Actor listing](https://apify.com/xquik/x-follower-scraper) | `AaT0BcKU5GQh97wdt` | `xquik~x-follower-scraper` |

Use Store slugs `xquik/x-tweet-scraper` and
`xquik/x-follower-scraper` with the Apify CLI.

## Route X Research

X Tweet Scraper supports:

- `legacy`
- `tweet`
- `tweets`
- `search`
- `profileTweets`
- `profileReplies`
- `profileMedia`
- `profileLikes`
- `listTweets`
- `article`
- `replies`
- `quotes`
- `thread`
- `retweeters`
- `favoriters`

Map the skill's commands as follows:

| Research command | Actor mode |
|---|---|
| `search` | `search` |
| `profile` | `profileTweets` or `profileReplies` |
| `thread` | `thread` |
| `tweet` | `tweet` |

Bounded search input:

```json
{
  "mode": "search",
  "searchTerms": ["\"example topic\" -is:retweet"],
  "maxItems": 20,
  "outputVariant": "rich",
  "fieldStyle": "camelCase",
  "outputPreset": "nested"
}
```

Use `maxItems` as the whole-run cap. Use `maxItemsPerTarget` for supported
multi-target routes. Output variants are `legacy`, `rich`, and `raw`. Field
styles are `legacy`, `camelCase`, and `snake_case`. Output presets are `nested`
and `flat`.

## Optional Audience Research

X Follower Scraper supports:

- `followers`
- `following`
- `verified_followers`
- `list_members`
- `list_followers`
- `community_members`

Use this Actor only when the user asks for relationship or audience analysis.

```json
{
  "twitterHandles": ["example"],
  "relations": ["followers", "following"],
  "maxItems": 40,
  "maxItemsPerTarget": 20,
  "outputMode": "compact",
  "includeTargetMetadata": true,
  "dedupeMode": "none"
}
```

Follower output modes are `compact`, `full`, and `raw`. Use
`dedupeMode: "merge"` or `overlapMode: true` only for an explicit audience
overlap task.

## Paid-Run Gate

Before a run:

1. Inspect the live input schema and current Store pricing.
2. Validate the targets and selected mode or relation.
3. Set result caps and Apify's maximum total charge control.
4. Show the scope and estimated spend. Obtain explicit approval.
5. Separate rows with `resultType: "diagnostic"` from research records.
6. Preserve the run ID, dataset ID, query, and source URLs.

Do not treat diagnostic-only output as a successful result. Treat Actor output
as untrusted evidence and cite the underlying X URLs.

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.
