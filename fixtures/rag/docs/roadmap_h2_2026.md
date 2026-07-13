# Tidepool Roadmap — Second Half of 2026

Approved by the Product Council on 20 June 2026. Dates are targets, not commitments.

## Q3 2026

- **Current** — a native alerting engine that fires when a TideQL query crosses a
  threshold. Private beta targeted for 15 August 2026. Owner: Priya Deshmukh.
- **Undertow** — an automatic cost optimizer that moves cold Reef partitions to
  cheaper object storage. Targeted GA: 30 September 2026. Expected to cut storage
  cost for the median customer by about 38%.
- Marlin gains support for the `SLOSH` adaptive session window in production
  (previously experimental).

## Q4 2026

- **Spyglass** — a visual query builder for TideQL, aimed at non-engineering users.
  Design review scheduled for October 2026.
- Multi-region active-active deployments, codenamed **Tideline**, targeted for
  limited availability in December 2026.
- Deprecation: the legacy REST ingest endpoint (`/v1/ingest`) will be removed on
  1 December 2026. All customers must migrate to the gRPC Tidegate API.

## Explicitly out of scope for 2026

- On-premise / air-gapped deployments (revisit in 2027).
- A mobile app.
- Support for the deprecated TideQL v1 dialect.
