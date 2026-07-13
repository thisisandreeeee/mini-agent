# Customer Case Study: Northwind Grocers

Northwind Grocers is a regional supermarket chain with 340 stores across the Pacific
Northwest. They adopted Tidepool in 2024 to power real-time inventory and cold-chain
monitoring.

## The challenge

Northwind's previous batch pipeline updated inventory dashboards every 30 minutes.
Spoilage in refrigerated aisles was detected too late, costing an estimated
$4.2 million per year in wasted stock.

## The deployment

- Northwind runs Tidepool in the `pacifica-2` region.
- They ingest roughly 8 billion events per day, mostly IoT temperature and
  point-of-sale events.
- Peak ingest is about 180,000 events per second, well within a single Marlin
  coordinator's limits.
- They wrote 47 continuous TideQL queries, including a `SLOSH`-windowed query that
  detects when a freezer's temperature trends upward over a shopping session.

## Results

- Cold-chain alert latency dropped from 30 minutes to under 2 seconds.
- Dashboard "time to first insight" (TTFI) measured at 640 milliseconds.
- Spoilage costs fell by an estimated 62% in the first year, saving roughly
  $2.6 million.
- Northwind's lead data engineer, Marcus Feld, presented these results at the
  Kestrel "HighTide" user conference in May 2026.

## Quote

"Tidepool turned our 30-minute guesswork into a live signal. We catch a failing
freezer before the ice cream even notices." — Marcus Feld, Northwind Grocers.
