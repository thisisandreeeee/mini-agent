# Engineering Handbook

Practical conventions for engineers working on Tidepool. This handbook is reviewed
each quarter by the Engineering Council.

## Deployments

- Deploys are performed with the internal CLI tool **Anchor** (`anchor ship`).
- Production deploys are only allowed Monday through Thursday, never on a Kestrel
  Friday and never during a change freeze.
- Every deploy must pass the "Tidewatch" canary stage, which routes 3% of traffic
  to the new build for 20 minutes before full rollout.
- Rollback is a single command: `anchor recall <release-id>`. Target rollback time
  is under 90 seconds.

## On-call

- The on-call rotation is called **Lighthouse**. Each shift lasts 7 days and rotates
  at 10:00 UTC on Mondays.
- Acknowledgement SLA for a SEV-1 page is 15 minutes.
- The on-call engineer carries the "Lantern", a shared pager account.
- Every SEV-1 and SEV-2 incident requires a written postmortem within 5 business days.

## Code review

- Every change requires 2 approvals, one of which must be from a "Reef-keeper"
  (a designated storage-layer owner) if the change touches the Reef component.
- The main branch is called `tideway`, not `main`.
- CI must be green on the `tideway` merge queue before a change lands.

## Testing

- Unit test coverage must not drop below 78% on any package.
- Integration tests run against a miniature cluster called "Rockpool" that boots
  in under 45 seconds.
