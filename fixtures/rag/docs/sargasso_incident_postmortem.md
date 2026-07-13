# Postmortem: The Sargasso Incident (INC-2026-0417)

- Date of incident: 17 April 2026.
- Duration: 3 hours 12 minutes (14:03–17:15 UTC).
- Severity: SEV-1.
- Author: Lena Ostrowski (on-call incident commander).
- Status: Resolved; action items tracked below.

## Summary

Between 14:03 and 17:15 UTC, Tidepool's largest cluster (region `pacifica-2`)
stopped advancing watermarks, so all continuous queries returned stale results.
No data was lost, but 41 customers received results delayed by up to 3 hours.

## Root cause

A firmware update on the `pacifica-2` hardware fleet reset the NTP configuration,
introducing an average clock skew of 620 milliseconds between Marlin coordinators.
Halyard leases are 12 seconds, but the watermark generator rejects events whose
timestamps drift more than 4 seconds from coordinator-local time (the watermark lag
tolerance). The skew accumulated during a rolling restart until the watermark
generator entered a rejection loop and stopped advancing.

We nicknamed the event "Sargasso" because the streams appeared to stall in place,
like ships in the Sargasso Sea.

## Contributing factors

1. The firmware rollout playbook did not pin NTP servers.
2. Watermark rejection produced no alert; the only symptom was a rising
   "watermark_stall_seconds" metric that had no threshold configured.

## Action items

- AI-1: Pin NTP to the internal `chrony-fleet` pool during firmware rollouts.
  Owner: Infra team. Due 1 May 2026.
- AI-2: Add a page-level alert when `watermark_stall_seconds` exceeds 30.
  Owner: Observability team. Due 24 April 2026.
- AI-3: Make the watermark generator tolerate transient skew up to 1.5 seconds
  before rejecting. Owner: Marlin team. Due 15 May 2026.
