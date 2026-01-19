# Dashboard Access Service Overview

## Access management for factory dashboards and internal systems

### Purpose

The Auth Service manages access to all internal factory dashboards and systems. It ensures that only authorized engineers, operators, and supervisors can view or modify machine telemetry, production line data, and quality reports.

This service is critical: if access fails, production monitoring and incident response are blocked.


### High-Level Architecture

* Operators and engineers authenticate via the Factory Portal

* Portal forwards requests to the Auth Service

* Auth Service validates credentials against the Employee Directory

* On success, the service issues a session token for dashboard and system access

Access tokens are used by downstream services to control read/write permissions across production line systems.



### Dependencies

* Employee Directory (LDAP)

* Redis (session cache)

* Factory Portal Frontend

* Key Management Service for token signing

Downtime in Redis or LDAP can affect authentication latency across all systems.



### Known Limitations

* Multi-plant active-active support is limited

* Token revocation is best-effort

* Legacy equipment interfaces may bypass RBAC



### Operational Notes

* Average authentication latency target: < 50ms

* P99 latency alert fires at 200ms

* Error budget is shared with Factory Portal

TODO: Document emergency rollback procedure for key rotation.



### Open Questions

* Should all plant-level dashboards migrate to short-lived tokens?

* Can we reduce Redis dependency for read-only access?
