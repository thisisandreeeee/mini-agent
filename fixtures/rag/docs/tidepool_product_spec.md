# Tidepool — Product Specification (v7.2)

Tidepool is Kestrel Analytics' real-time stream analytics platform. This document
describes the internal architecture and published limits for the 7.2 release
(shipped 4 February 2026).

## Core components

- **Marlin** — the distributed query engine. Marlin executes continuous SQL-like
  queries over live event streams.
- **Reef** — the columnar storage layer. Reef retains raw events for 90 days by
  default and downsampled rollups for 3 years.
- **Driftwood** — the internal message bus that carries events between ingestion
  and Marlin. Driftwood replaced Apache Kafka in the 5.0 release (see ADR-014).
- **Tidegate** — the ingestion gateway that authenticates and rate-limits producers.

## Published limits (per node)

- Maximum sustained ingest: 2.4 million events per second per node.
- Maximum query fan-out: 512 concurrent continuous queries per Marlin coordinator.
- Maximum single event size: 256 KiB.
- Default watermark lag tolerance: 4 seconds.

## The Halyard consensus protocol

Marlin coordinators agree on partition ownership using **Halyard**, Kestrel's
in-house consensus protocol. Halyard uses a quorum of 5 coordinators and a lease
duration of 12 seconds. Halyard is a variant of Raft modified to tolerate up to
2 simultaneous coordinator failures without losing a quorum.

## Query language

Tidepool queries are written in **TideQL**. A TideQL query always begins with the
keyword `STREAM` rather than `SELECT`. Window functions use the `TUMBLE`, `HOP`,
and `SLOSH` keywords; `SLOSH` is a Kestrel-specific adaptive session window that
grows its gap based on observed event cadence.
