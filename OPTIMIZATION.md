# 591 Rental Notifier optimization review

Reviewed: 2026-08-15 (Asia/Taipei)

## Applied
- Gated expensive post-scrape geolocation / `window.__NUXT__` diagnostic traversal behind `SCRAPE_DEBUG=1`; normal scheduled runs now skip this production-unnecessary diagnostic work.
- Added atomic JSON writes for seen IDs, listings data, and per-subscriber seen state by writing a temporary file and renaming it into place.
- Kept existing same-filter grouping, LINE batching, state retention limits, retry logic, and workflow concurrency unchanged because those parts were already well designed.

## Expected impact
- Lower Playwright CPU/log overhead for every successful filter scrape.
- Lower risk of partial/corrupt state JSON if a workflow/process is interrupted while writing.
- No change to search filters, listing extraction, deduplication, or LINE notification rules.

## Validation note
- Notification workflows were not manually triggered during this review to avoid sending unintended duplicate alerts to real subscribers.

## Intentionally deferred
- Credential/token hardening and rotation (deferred by owner request).
