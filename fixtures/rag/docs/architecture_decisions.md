# Architecture Decision Records (ADRs)

This document records significant architecture decisions for the Tidepool platform.
Each ADR is immutable once accepted.

## ADR-014: Replace Kafka with Driftwood

- Status: Accepted (18 August 2022).
- Decision: Build an in-house message bus, Driftwood, to replace Apache Kafka.
- Rationale: Kafka's partition rebalancing caused ingest stalls of up to 40 seconds
  during Marlin coordinator restarts. Driftwood uses sticky partition leases tied to
  the Halyard protocol, reducing rebalance stalls to under 800 milliseconds.
- Trade-off: Kestrel now maintains its own bus, adding an estimated 1.5 engineer-years
  of ongoing maintenance.

## ADR-021: Adopt Halyard for coordinator consensus

- Status: Accepted (2 March 2023).
- Decision: Use the Halyard consensus protocol (a modified Raft) for Marlin
  coordinator partition ownership.
- Rationale: Standard Raft tolerates only 1 failure in a 3-node quorum. Kestrel's
  largest customer deployments require surviving 2 simultaneous availability-zone
  failures, so Halyard uses a 5-coordinator quorum with 12-second leases.

## ADR-029: Reef switches from row storage to columnar

- Status: Accepted (14 November 2024).
- Decision: Rewrite the Reef storage layer to use a columnar format ("Nautilus
  blocks") instead of row-oriented storage.
- Rationale: Analytical rollup queries scanned 6x more data than necessary under the
  row format. Nautilus blocks reduced rollup query cost by roughly 71% in benchmarks.
- Trade-off: Point lookups by event ID became ~3x slower, deemed acceptable because
  Tidepool workloads are 95% analytical.

## ADR-033: Reject GraphQL for the public API

- Status: Rejected (9 January 2025).
- Decision: Do NOT adopt GraphQL for Tidepool's public API; stay with gRPC.
- Rationale: GraphQL's flexible queries made per-tenant rate limiting in Tidegate
  unpredictable. gRPC with fixed method costs keeps rate-limit accounting simple.
