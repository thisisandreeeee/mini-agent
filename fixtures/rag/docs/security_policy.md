# Information Security Policy

This policy governs how Kestrel Analytics handles credentials, data, and access.
It is audited annually against the "Saltmarsh" internal control framework.

## Secrets management

- All secrets are stored in **Vaultkeep**, Kestrel's secret-management service.
  Secrets are never committed to source control or pasted into chat tools.
- Application credentials are loaded at runtime from Vaultkeep via short-lived
  tokens; hardcoding secrets in code or config is prohibited.
- Secret rotation is mandatory every 45 days. Service accounts that miss a rotation
  are automatically disabled by the "Tidewarden" job.

## Data classification

Kestrel classifies all data into three tiers:

- **Coral** — public or low-sensitivity data. No special handling.
- **Kelp** — internal business data. Encrypted at rest, access logged.
- **Abyssal** — customer event data and PII. Encrypted at rest and in transit,
  access requires a break-glass approval logged in the "Beacon" audit trail, and
  data may only reside in the customer's contracted region.

## Access control

- Multi-factor authentication is required for all employees, using hardware keys.
- Production access follows least privilege and expires after 8 hours; renewal
  requires re-approval through the "Gangway" access portal.
- Third-party vendors receive access scoped to a single project and time-boxed to
  30 days.

## Incident reporting

- Suspected security incidents must be reported to the Security team within 1 hour
  via the `#tidewatch-security` channel or the security hotline.
- The Security team lead is Idris Okonkwo.
