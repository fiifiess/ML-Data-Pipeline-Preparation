# Postmortem: Machine Log Search Outage Runbook (November 2023)

## Steps for when engineers cannot search machine logs or defect records

### Summary

On November 14, 2023, the machine telemetry search service experienced an outage lasting approximately 47 minutes. Engineers could not search machine logs or defect records for production lines, delaying troubleshooting.

The issue was first noticed via operator reports before automated alerts triggered.

### Timeline

* 09:12 UTC — Deployment of Telemetry Search Service v3.8

* 09:18 UTC — Error rates begin to increase

* 09:25 UTC — First operator reports received

* 09:31 UTC — On-call engineer paged

* 09:47 UTC — Rollback initiated

* 09:59 UTC — Error rates return to baseline

### Root Cause

A configuration change in v3.8 increased memory usage during search indexing. Under normal production load, this caused repeated container restarts due to out-of-memory errors.

The change was not covered by existing load tests.

### What Went Well

* Rollback procedure restored service within 12 minutes

* On-call response time met SLA

* No machine telemetry data was lost

### What Went Wrong

* Alert thresholds were too lenient to detect memory spikes early

* Deployment occurred during peak production hours

* No canary deployment was used

Confusion about ownership between Factory Operations and Platform teams also delayed initial triage.

### Action Items

* Add memory stress tests to CI pipeline

* Tighten alert thresholds for search service

* Enforce canary deployments for telemetry services

* Update ownership and escalation documentation

Some action items are still in progress.