# Telemetry Data Latency Runbook

## Steps for when machine sensor data or dashboard updates are slow

### Symptoms

* Factory dashboards respond slowly

* Requests to machine telemetry APIs time out

* Supervisors report delays in production monitoring

Latency issues often appear before critical incidents on the production line.


### Immediate Checks

* Inspect Factory Portal and API dashboards

* Compare request volumes against baseline

* Check Auth Service latency (often a bottleneck)

* Inspect database connection pools for saturation

If dashboards are down, use CLI metrics snapshots.


### Common Causes

* Sudden spikes in production line data ingestion

* Misconfigured rate limits on APIs

* Slow responses from CNC or stamping machines

* Database connection exhaustion

Some latency spikes may be caused by maintenance or batch jobs; always verify traffic source.


### Mitigation Steps

* Enable temporary rate limiting for non-critical endpoints

* Scale API servers or queue workers

* Restart unhealthy service pods if necessary

* Disable non-critical telemetry streaming temporarily

Escalate if latency does not decrease within 10 minutes.


### Escalation

* Page on-call SRE if P99 > 500ms for 5 minutes

* Notify Production Management if operators are impacted

* Open an incident bridge for sustained latency


### Known False Positives

* Scheduled load tests on factory systems

* High-volume batch jobs generating telemetry bursts

Always confirm traffic source before declaring an incident.